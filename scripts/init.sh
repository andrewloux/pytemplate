#!/bin/bash
# Simple project initialization script that recursively searches for placeholders
# Usage: ./scripts/init.sh <project_name>

set -e  # Exit on error

# Check if a project name was provided
if [ $# -ne 1 ]; then
    echo "Error: You must provide a project name."
    echo "Usage: ./scripts/init.sh <project_name>"
    exit 1
fi

PROJECT_NAME=$1

# Validate project name (lowercase with underscores)
if ! [[ $PROJECT_NAME =~ ^[a-z][a-z0-9_]*$ ]]; then
    echo "Error: Invalid project name '$PROJECT_NAME'."
    echo "Project name must start with a letter and contain only lowercase letters, numbers, and underscores."
    exit 1
fi

# Check if project is already initialized by looking for placeholders
if ! grep -q "\${PROJECT_NAME}" pyproject.toml 2>/dev/null; then
    echo "Error: Project already initialized or pyproject.toml not found."
    exit 1
fi

echo "Initializing project with name: $PROJECT_NAME"

# Find and replace placeholders in all text files recursively
echo "Updating project files..."

# Find all text files (excluding .git directory) that contain the placeholder
for file in $(grep -l "\${PROJECT_NAME}" --include="*.py" --include="*.toml" --include="*.xml" --include="*.md" --include="*.txt" -r . 2>/dev/null); do
    # Use different sed syntax depending on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/\${PROJECT_NAME}/$PROJECT_NAME/g" "$file"
    else
        # Linux
        sed -i "s/\${PROJECT_NAME}/$PROJECT_NAME/g" "$file"
    fi
    echo "Updated: $file"
done

# Rename the PyCharm module file if it exists
if [ -f ".idea/\${PROJECT_NAME}.iml" ]; then
    mv ".idea/\${PROJECT_NAME}.iml" ".idea/$PROJECT_NAME.iml"
    echo "Renamed: .idea/\${PROJECT_NAME}.iml -> .idea/$PROJECT_NAME.iml"
    
    # Update the module reference in modules.xml if it exists
    if [ -f ".idea/modules.xml" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/\${PROJECT_NAME}.iml/$PROJECT_NAME.iml/g" ".idea/modules.xml"
        else
            sed -i "s/\${PROJECT_NAME}.iml/$PROJECT_NAME.iml/g" ".idea/modules.xml"
        fi
    fi
fi

# Setup virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
    echo "Virtual environment created at .venv/"
fi

echo ""
echo "Project initialized successfully!"
echo "Project name set to: $PROJECT_NAME"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Install dependencies:"
echo "   # For regular setup"
echo "   uv run init"
echo ""
echo "   # For development setup (includes all dev tools)"
echo "   uv run devinit"