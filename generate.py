#!/usr/bin/env python3
"""
Manim Actor Video Generator CLI

Simple command-line tool to generate videos with actors.

Usage:
    python generate.py --scene ActorIntroduction --quality low
    python generate.py --scene MathLesson --quality high --preview
    python generate.py --list
"""

import argparse
import subprocess
import sys
from pathlib import Path


def list_available_scenes():
    """List all available scenes."""
    print("\n=== Available Scenes ===\n")

    print("Basic Examples (scenes/basic_examples.py):")
    basic_scenes = [
        ("ActorIntroduction", "Introduction to all actor styles"),
        ("SimplePresentation", "Actor presents a simple concept"),
        ("MathLesson", "Actor teaches the Pythagorean theorem"),
        ("ActorInteraction", "Actor interacts with animated objects")
    ]

    for scene, description in basic_scenes:
        print(f"  • {scene:<25} - {description}")

    print("\nAdvanced Examples (scenes/advanced_examples.py):")
    advanced_scenes = [
        ("ProblemSolving", "Actor works through a math problem"),
        ("MultiActorScene", "Two actors have a conversation"),
        ("InteractiveTutorial", "Comprehensive interactive tutorial")
    ]

    for scene, description in advanced_scenes:
        print(f"  • {scene:<25} - {description}")

    print("\n")


def get_quality_flag(quality: str) -> str:
    """Convert quality string to manim flag."""
    quality_map = {
        "low": "-ql",
        "medium": "-qm",
        "high": "-qh",
        "production": "-qk"
    }
    return quality_map.get(quality.lower(), "-ql")


def generate_video(scene_name: str, quality: str, preview: bool, output_dir: str):
    """
    Generate a video using Manim.

    Args:
        scene_name: Name of the scene class
        quality: Quality level (low, medium, high, production)
        preview: Whether to preview after rendering
        output_dir: Output directory for video
    """
    # Determine which file contains the scene
    basic_scenes = ["ActorIntroduction", "SimplePresentation", "MathLesson", "ActorInteraction"]
    advanced_scenes = ["ProblemSolving", "MultiActorScene", "InteractiveTutorial"]

    if scene_name in basic_scenes:
        scene_file = "scenes/basic_examples.py"
    elif scene_name in advanced_scenes:
        scene_file = "scenes/advanced_examples.py"
    else:
        print(f"Error: Scene '{scene_name}' not found.")
        print("Run with --list to see available scenes.")
        sys.exit(1)

    # Build manim command
    quality_flag = get_quality_flag(quality)
    preview_flag = "-p" if preview else ""

    cmd = [
        "manim",
        quality_flag,
        preview_flag,
        scene_file,
        scene_name
    ]

    if output_dir:
        cmd.extend(["--media_dir", output_dir])

    # Remove empty strings
    cmd = [c for c in cmd if c]

    print(f"\n=== Generating Video ===")
    print(f"Scene: {scene_name}")
    print(f"Quality: {quality}")
    print(f"Preview: {preview}")
    print(f"Command: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, check=True, text=True)
        print("\n✓ Video generated successfully!")

        if not preview:
            print(f"\nVideo saved in: media/videos/{scene_file}/{quality}/")

    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error generating video: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n✗ Error: Manim is not installed or not in PATH.")
        print("Install with: pip install manim")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Manim Actor Video Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py --list
  python generate.py --scene ActorIntroduction --quality low --preview
  python generate.py --scene MathLesson --quality high
  python generate.py --scene MultiActorScene --quality medium --preview
        """
    )

    parser.add_argument(
        "--scene",
        type=str,
        help="Name of the scene to render"
    )

    parser.add_argument(
        "--quality",
        type=str,
        choices=["low", "medium", "high", "production"],
        default="low",
        help="Video quality (default: low)"
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview video after rendering"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Output directory for videos"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available scenes"
    )

    args = parser.parse_args()

    # Show banner
    print("\n" + "="*50)
    print(" Manim Actor Video Generator")
    print("="*50)

    if args.list:
        list_available_scenes()
        sys.exit(0)

    if not args.scene:
        print("\nError: --scene is required")
        print("Run with --list to see available scenes")
        parser.print_help()
        sys.exit(1)

    generate_video(args.scene, args.quality, args.preview, args.output)


if __name__ == "__main__":
    main()
