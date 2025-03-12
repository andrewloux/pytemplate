#!/usr/bin/env python3
"""
Task runner for ${PROJECT_NAME}.
Usage:
    uv run tasks.py init          # Initialize the project with regular setup
    uv run tasks.py devinit       # Initialize the project with development tools
    uv run tasks.py format        # Format code using black
    uv run tasks.py check         # Type check using mypy
    uv run tasks.py test          # Run tests using pytest
    uv run tasks.py test-cov      # Run tests with coverage
"""

import os
import sys
import subprocess
from typing import List, Optional, Dict, Callable


def run_command(cmd: List[str], cwd: Optional[str] = None) -> None:
    """Run a command and print its output."""
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def init_task(args: List[str]) -> None:
    """Initialize the project with regular setup."""
    run_command(["pip", "install", "-U", "pip", "uv"])
    run_command(["uv", "pip", "install", "-e", "."])
    print("\nProject initialized successfully!")


def devinit_task(args: List[str]) -> None:
    """Initialize the project with development tools."""
    run_command(["pip", "install", "-U", "pip", "uv"])
    run_command(["uv", "pip", "install", "-e", ".[dev]"])
    print("\nProject initialized for development successfully!")


def format_task(args: List[str]) -> None:
    """Format code using black."""
    run_command(["black", "src/", "tests/"])


def check_task(args: List[str]) -> None:
    """Type check using mypy."""
    run_command(["mypy", "src/", "tests/"])


def test_task(args: List[str]) -> None:
    """Run tests using pytest."""
    run_command(["pytest", "tests/"])


def test_cov_task(args: List[str]) -> None:
    """Run tests with coverage."""
    run_command(["pytest", "--cov=src", "tests/"])


# Task registry
TASKS: Dict[str, Callable[[List[str]], None]] = {
    "init": init_task,
    "devinit": devinit_task,
    "format": format_task,
    "check": check_task,
    "test": test_task,
    "test-cov": test_cov_task,
}


def print_help() -> None:
    """Print help message."""
    print(__doc__)
    print("Available tasks:")
    for task_name, task_func in TASKS.items():
        print(f"  {task_name:<10} - {task_func.__doc__}")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    task_name = sys.argv[1]
    task_args = sys.argv[2:]

    if task_name not in TASKS:
        print(f"Unknown task: {task_name}")
        print_help()
        sys.exit(1)

    # Run the task
    TASKS[task_name](task_args)


if __name__ == "__main__":
    main()
