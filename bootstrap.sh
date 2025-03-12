#!/bin/bash
# Bootstrap script for initializing the project
# Usage: ./bootstrap.sh <project_name>

set -e  # Exit on error

if [ $# -ne 1 ]; then
    echo "Error: You must provide a project name."
    echo "Usage: ./bootstrap.sh <project_name>"
    exit 1
fi

PROJECT_NAME=$1

# Install poethepoet first
echo "Installing poethepoet..."
uv pip install poethepoet

# Run the initialization script
echo "Initializing project as: $PROJECT_NAME"
uv run -- python scripts/init_project.py "$PROJECT_NAME"

# Install dependencies and setup
echo "Installing dependencies and setting up project..."
uv pip install -e .[dev]

# Run format and check
echo "Formatting code and running type checks..."
uv run poe format
uv run poe check

echo ""
echo "✅ Project successfully bootstrapped as: $PROJECT_NAME"
echo "You can now run tasks with: uv run poe <task-name>"
echo ""
echo "Available tasks:"
uv run poe --help
