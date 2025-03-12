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
        print("Project name must start with a letter and contain only lowercase letters, numbers, and underscores.")
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
                new_content = content.replace("${PROJECT_NAME}.iml", f"{project_name}.iml")
                modules_xml.write_text(new_content)
                print(f"Updated module reference in: {modules_xml}")


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
    if not pyproject_toml.exists() or "${PROJECT_NAME}" not in pyproject_toml.read_text():
        print("Error: Project already initialized or pyproject.toml not found.")
        sys.exit(1)
        
    print(f"Initializing project with name: {project_name}")
    
    # Find files with placeholder
    print("Searching for files with placeholder...")
    files_with_placeholder = find_files_with_placeholder(root_dir)
    
    # Replace placeholder in files
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
