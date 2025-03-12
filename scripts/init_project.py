#!/usr/bin/env python3
"""Project initialization script for replacing placeholders.

This script recursively searches for ${PROJECT_NAME} placeholders and replaces them
with the provided project name.

Usage:
    uv run scripts/init_project.py <project_name>
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from typing import List, Set, Tuple


def validate_project_name(name: str) -> bool:
    """Validate that the project name is suitable for a Python package.

    Args:
        name: The project name to validate

    Returns:
        True if the name is valid, False otherwise
    """
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        print(f"Error: Invalid project name '{name}'.")
        print(
            "Project name must start with a letter and contain only lowercase letters, numbers, and underscores."
        )
        return False
    return True


def find_files_with_placeholder(root_dir: Path) -> List[Path]:
    """Find all files containing the PROJECT_NAME placeholder.

    Args:
        root_dir: The root directory to search

    Returns:
        A list of file paths containing the placeholder
    """
    placeholder = "${PROJECT_NAME}"
    files_with_placeholder = []

    # Extensions to search
    text_extensions = {".py", ".toml", ".xml", ".md", ".txt", ".iml"}

    # Directories to skip
    skip_dirs = {".git", ".venv", "__pycache__"}

    for path in root_dir.glob("**/*"):
        # Skip directories in skip_dirs
        if path.is_dir() and path.name in skip_dirs:
            continue

        # Only check files with text extensions
        if path.is_file() and path.suffix in text_extensions:
            try:
                content = path.read_text()
                if placeholder in content:
                    files_with_placeholder.append(path)
            except UnicodeDecodeError:
                # Skip binary files
                pass

    return files_with_placeholder


def replace_placeholder_in_files(files: List[Path], project_name: str) -> int:
    """Replace the PROJECT_NAME placeholder in the specified files.

    Args:
        files: List of files to process
        project_name: The name to replace the placeholder with

    Returns:
        The number of files updated
    """
    count = 0
    placeholder = "${PROJECT_NAME}"

    for file in files:
        content = file.read_text()
        if placeholder in content:
            new_content = content.replace(placeholder, project_name)
            file.write_text(new_content)
            print(f"Updated: {file}")
            count += 1

    return count


def rename_project_files(root_dir: Path, project_name: str) -> None:
    """Rename files that contain the placeholder in their names.

    Args:
        root_dir: The root directory
        project_name: The project name to use
    """
    # Check for PyCharm files to rename
    idea_dir = root_dir / ".idea"
    if idea_dir.exists():
        placeholder_iml = idea_dir / "${PROJECT_NAME}.iml"
        if placeholder_iml.exists():
            new_iml = idea_dir / f"{project_name}.iml"
            placeholder_iml.rename(new_iml)
            print(f"Renamed: {placeholder_iml} -> {new_iml}")

            # Update modules.xml if it exists
            modules_xml = idea_dir / "modules.xml"
            if modules_xml.exists():
                content = modules_xml.read_text()
                new_content = content.replace(
                    "${PROJECT_NAME}.iml", f"{project_name}.iml"
                )
                modules_xml.write_text(new_content)
                print(f"Updated module reference in: {modules_xml}")


def check_project_initialized(pyproject_path: Path) -> bool:
    """Check if the project has already been initialized.

    Args:
        pyproject_path: Path to pyproject.toml

    Returns:
        True if project is already initialized, False otherwise
    """
    if not pyproject_path.exists():
        return False

    content = pyproject_path.read_text()
    # Check for either the old placeholder or the new placeholder
    return "${PROJECT_NAME}" not in content and "python_project_template" not in content


def main():
    """Main entry point."""
    # Check for arguments
    if len(sys.argv) != 2:
        print("Error: You must provide a project name.")
        print(f"Usage: {sys.argv[0]} <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]

    # Validate the project name
    if not validate_project_name(project_name):
        sys.exit(1)

    # Get the root directory (one level up from scripts)
    root_dir = Path(__file__).parent.parent.absolute()

    # Check if project is already initialized
    pyproject_toml = root_dir / "pyproject.toml"
    if not pyproject_toml.exists():
        print("Error: pyproject.toml not found.")
        sys.exit(1)

    content = pyproject_toml.read_text()
    already_initialized = check_project_initialized(pyproject_toml)

    if already_initialized:
        print("Warning: Project appears to already be initialized.")
        print(
            f"Continuing will replace the current project name with '{project_name}'."
        )
        response = input("Do you want to continue? (y/N): ")
        if response.lower() not in ["y", "yes"]:
            print("Initialization cancelled.")
            sys.exit(0)

    # Find placeholder - check both the old and new placeholder format
    placeholders_found = False
    if "${PROJECT_NAME}" in content:
        placeholders_found = True
    elif "python_project_template" in content:
        placeholders_found = True
        # Update our placeholder finding function to also look for the new placeholder
        global find_files_with_placeholder
        old_find = find_files_with_placeholder

        def new_find(root_dir):
            """Wrapper to search for both placeholder formats."""
            files1 = old_find(root_dir)  # Find old format

            # Add function to find new format
            files2 = []
            for path in root_dir.glob("**/*"):
                if path.is_dir() and path.name in {".git", ".venv", "__pycache__"}:
                    continue
                if path.is_file() and path.suffix in {
                    ".py",
                    ".toml",
                    ".xml",
                    ".md",
                    ".txt",
                    ".iml",
                }:
                    try:
                        file_content = path.read_text()
                        if "python_project_template" in file_content:
                            files2.append(path)
                    except UnicodeDecodeError:
                        pass

            # Combine unique files
            return list(set(files1 + files2))

        find_files_with_placeholder = new_find

        # Also update the replacement function to handle the new placeholder
        global replace_placeholder_in_files
        old_replace = replace_placeholder_in_files

        def new_replace(files, project_name):
            """Wrapper to replace both placeholder formats."""
            count = 0
            for file in files:
                content = file.read_text()
                if "${PROJECT_NAME}" in content or "python_project_template" in content:
                    new_content = content.replace("${PROJECT_NAME}", project_name)
                    new_content = new_content.replace(
                        "python_project_template", project_name
                    )
                    file.write_text(new_content)
                    print(f"Updated: {file}")
                    count += 1
            return count

        replace_placeholder_in_files = new_replace

    if not placeholders_found:
        print("Error: No template placeholders found in pyproject.toml.")
        print(
            "This may not be a template project or it may already be fully initialized."
        )
        sys.exit(1)

    print(f"Initializing project with name: {project_name}")

    # Find files with placeholders
    print("Searching for files with placeholders...")
    files_with_placeholder = find_files_with_placeholder(root_dir)

    if not files_with_placeholder:
        print("Warning: No files with placeholders found.")
        print("The project may already be initialized.")
        sys.exit(1)

    # Replace placeholders in files
    print("Updating project files...")
    count = replace_placeholder_in_files(files_with_placeholder, project_name)

    # Rename any files that contain the placeholder
    rename_project_files(root_dir, project_name)

    print(f"\nProject initialization completed!")
    print(f"Updated {count} files with project name: {project_name}")
    print("\nNext step: Set up your development environment")
    print("Run: uv pip install -e .[dev] && uv run poe setup")


if __name__ == "__main__":
    main()
