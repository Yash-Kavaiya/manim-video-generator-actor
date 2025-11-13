#!/usr/bin/env python3
"""
Validation script for Apify Actor schemas and configurations.
This script verifies that all required schemas are present and properly configured.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}\n")


def print_success(text: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def validate_json_file(file_path: Path, file_description: str) -> Tuple[bool, Dict]:
    """
    Validate that a file exists and contains valid JSON.

    Returns:
        Tuple of (success: bool, data: dict)
    """
    if not file_path.exists():
        print_error(f"{file_description} not found at: {file_path}")
        return False, {}

    try:
        with open(file_path) as f:
            data = json.load(f)
        print_success(f"{file_description} found and valid JSON")
        return True, data
    except json.JSONDecodeError as e:
        print_error(f"{file_description} contains invalid JSON: {e}")
        return False, {}


def validate_actor_json(data: Dict) -> List[str]:
    """Validate actor.json structure and return list of issues."""
    issues = []

    # Check required fields
    required_fields = ['actorSpecification', 'name', 'title', 'version']
    for field in required_fields:
        if field not in data:
            issues.append(f"Missing required field: {field}")
        else:
            print_success(f"Has {field}: {data[field]}")

    # Check input schema reference
    if 'input' not in data:
        issues.append("Missing 'input' field (should reference INPUT_SCHEMA.json)")
    else:
        print_success(f"Input schema reference: {data['input']}")

    # Check storages configuration
    if 'storages' not in data:
        print_warning("No 'storages' configuration found")
    else:
        print_success("Has 'storages' configuration")

        # Check dataset schema
        if 'dataset' in data['storages']:
            dataset_config = data['storages']['dataset']
            print_success(f"Dataset schema defined: {dataset_config.get('title', 'Untitled')}")

            if 'views' in dataset_config:
                views = list(dataset_config['views'].keys())
                print_success(f"Dataset views: {', '.join(views)}")
            else:
                print_warning("No dataset views defined")
        else:
            print_warning("No dataset schema defined in storages")

    return issues


def validate_input_schema(data: Dict) -> List[str]:
    """Validate INPUT_SCHEMA.json structure and return list of issues."""
    issues = []

    # Check schema version
    if 'schemaVersion' not in data:
        issues.append("Missing 'schemaVersion' field")
    else:
        print_success(f"Schema version: {data['schemaVersion']}")

    # Check title
    if 'title' not in data:
        issues.append("Missing 'title' field")
    else:
        print_success(f"Schema title: {data['title']}")

    # Check type
    if 'type' not in data:
        issues.append("Missing 'type' field")
    elif data['type'] != 'object':
        print_warning(f"Schema type is '{data['type']}', expected 'object'")
    else:
        print_success(f"Schema type: {data['type']}")

    # Check properties
    if 'properties' not in data:
        issues.append("Missing 'properties' field")
    else:
        properties = data['properties']
        print_success(f"Number of properties: {len(properties)}")

        # Validate each property
        property_issues = []
        for prop_name, prop_config in properties.items():
            if 'type' not in prop_config:
                property_issues.append(f"Property '{prop_name}' missing 'type' field")
            if 'title' not in prop_config:
                property_issues.append(f"Property '{prop_name}' missing 'title' field")

        if property_issues:
            for issue in property_issues:
                print_warning(issue)
        else:
            print_success("All properties properly configured")

    # Check required fields
    if 'required' in data:
        print_success(f"Required fields: {', '.join(data['required'])}")
    else:
        print_warning("No required fields specified")

    return issues


def validate_input_json(data: Dict, schema: Dict) -> List[str]:
    """Validate input.json against the schema."""
    issues = []

    if not data:
        issues.append("input.json is empty")
        return issues

    # Check if required fields from schema are present
    required_fields = schema.get('required', [])
    for field in required_fields:
        if field not in data:
            issues.append(f"Missing required field in sample input: {field}")
        else:
            print_success(f"Has required field '{field}': {data[field]}")

    # Check if sample input fields match schema properties
    schema_properties = schema.get('properties', {})
    for field in data.keys():
        if field not in schema_properties:
            print_warning(f"Sample input has field '{field}' not defined in schema")

    return issues


def main():
    """Main validation function."""
    print_header("Apify Actor Schema Validation")

    base_path = Path(__file__).parent / '.actor'
    all_valid = True

    # Validate actor.json
    print_header("Validating actor.json")
    actor_json_path = base_path / 'actor.json'
    actor_valid, actor_data = validate_json_file(actor_json_path, "actor.json")

    if actor_valid:
        actor_issues = validate_actor_json(actor_data)
        if actor_issues:
            print("\n" + Colors.RED + "Issues found in actor.json:" + Colors.END)
            for issue in actor_issues:
                print_error(issue)
            all_valid = False
    else:
        all_valid = False

    # Validate INPUT_SCHEMA.json
    print_header("Validating INPUT_SCHEMA.json")
    input_schema_path = base_path / 'INPUT_SCHEMA.json'
    schema_valid, schema_data = validate_json_file(input_schema_path, "INPUT_SCHEMA.json")

    if schema_valid:
        schema_issues = validate_input_schema(schema_data)
        if schema_issues:
            print("\n" + Colors.RED + "Issues found in INPUT_SCHEMA.json:" + Colors.END)
            for issue in schema_issues:
                print_error(issue)
            all_valid = False
    else:
        all_valid = False

    # Validate input.json (sample input)
    print_header("Validating input.json (Sample Input)")
    input_json_path = base_path / 'input.json'
    input_valid, input_data = validate_json_file(input_json_path, "input.json")

    if input_valid and schema_valid:
        input_issues = validate_input_json(input_data, schema_data)
        if input_issues:
            print("\n" + Colors.YELLOW + "Issues found in input.json:" + Colors.END)
            for issue in input_issues:
                print_warning(issue)
    elif not input_valid:
        all_valid = False

    # Check if INPUT_SCHEMA.json is referenced correctly in actor.json
    print_header("Validating Schema References")
    if actor_valid and 'input' in actor_data:
        input_ref = actor_data['input']
        expected_path = base_path / input_ref.lstrip('./')

        if expected_path.exists():
            print_success(f"Input schema reference is correct: {input_ref}")
        else:
            print_error(f"Input schema reference points to non-existent file: {input_ref}")
            print_error(f"Expected path: {expected_path}")
            all_valid = False

    # Final summary
    print_header("Validation Summary")

    if all_valid:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All validations passed!{Colors.END}")
        print(f"\n{Colors.GREEN}Your Actor configuration is complete and valid.{Colors.END}")
        print(f"{Colors.GREEN}You can safely remove the maintenance flag.{Colors.END}")
        print(f"\n{Colors.BLUE}Next steps:{Colors.END}")
        print("1. Go to Apify Console")
        print("2. Navigate to your Actor's Publication tab")
        print("3. Toggle OFF the maintenance mode")
        print("4. Save changes")
        print(f"\n{Colors.BLUE}For detailed instructions, see: REMOVE_MAINTENANCE_FLAG.md{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Validation failed!{Colors.END}")
        print(f"\n{Colors.RED}Please fix the issues above before removing the maintenance flag.{Colors.END}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
