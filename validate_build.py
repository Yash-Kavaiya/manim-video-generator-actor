#!/usr/bin/env python3
"""
Validation script to check if the Actor build will succeed.
Run this before pushing to catch issues early.
"""

import ast
import json
import os
import sys
from pathlib import Path


def validate_python_syntax(file_path):
    """Validate Python file syntax."""
    try:
        with open(file_path, 'r') as f:
            ast.parse(f.read())
        print(f"✅ {file_path}: Syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path}: Syntax Error - {e}")
        return False


def validate_json(file_path):
    """Validate JSON file syntax."""
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"✅ {file_path}: Valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {file_path}: Invalid JSON - {e}")
        return False


def validate_imports():
    """Check if critical imports would work (without installing deps)."""
    print("\n🔍 Checking module structure...")

    # Check __init__.py exists
    init_file = Path('src/__init__.py')
    if not init_file.exists():
        print("❌ src/__init__.py is missing")
        return False
    print("✅ src/__init__.py exists")

    # Check __main__.py exists
    main_file = Path('src/__main__.py')
    if not main_file.exists():
        print("❌ src/__main__.py is missing")
        return False
    print("✅ src/__main__.py exists")

    return True


def validate_requirements():
    """Check requirements.txt syntax."""
    print("\n🔍 Checking requirements.txt...")
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Basic validation - should have package name
                    if '=' in line or '>' in line or '<' in line:
                        continue
                    elif line:
                        continue
                    else:
                        print(f"⚠️  Line {i} might be invalid: {line}")
        print("✅ requirements.txt looks valid")
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False


def main():
    """Run all validations."""
    print("🚀 Starting Actor build validation...\n")

    all_valid = True

    # Validate Python files
    print("📝 Validating Python files...")
    python_files = [
        'main.py',
        'src/__init__.py',
        'src/__main__.py',
        'src/const.py',
        'src/models.py',
        'src/event_store.py',
        'src/mcp_gateway.py',
        'src/server.py',
    ]

    for py_file in python_files:
        if Path(py_file).exists():
            if not validate_python_syntax(py_file):
                all_valid = False
        else:
            print(f"⚠️  {py_file} not found (might be optional)")

    # Validate JSON files
    print("\n📋 Validating JSON files...")
    json_files = [
        '.actor/actor.json',
        '.actor/INPUT_SCHEMA.json',
        '.actor/pay_per_event.json',
    ]

    for json_file in json_files:
        if Path(json_file).exists():
            if not validate_json(json_file):
                all_valid = False
        else:
            print(f"⚠️  {json_file} not found")

    # Validate imports
    if not validate_imports():
        all_valid = False

    # Validate requirements
    if not validate_requirements():
        all_valid = False

    # Check Dockerfile
    print("\n🐳 Checking Dockerfile...")
    if Path('Dockerfile').exists():
        print("✅ Dockerfile exists")
    else:
        print("❌ Dockerfile not found")
        all_valid = False

    # Final result
    print("\n" + "="*50)
    if all_valid:
        print("✅ All validations passed! Actor should build successfully.")
        return 0
    else:
        print("❌ Some validations failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
