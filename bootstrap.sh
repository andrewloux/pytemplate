#!/bin/bash
# Bootstrap script for initializing the project
# Usage: ./bootstrap.sh <project_name>

set -e  # Exit on error

# Print colorful status messages
info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# Check for project name argument
if [ $# -ne 1 ]; then
    error "You must provide a project name."
    echo "Usage: ./bootstrap.sh <project_name>"
    exit 1
fi

PROJECT_NAME=$1

# Make sure we're in the template root directory
if [ ! -f "pyproject.toml" ]; then
    error "Could not find pyproject.toml in the current directory."
    error "Make sure you're running this script from the template root directory."
    exit 1
fi

# Check if project contains placeholder or is already initialized
if ! grep -q "python_project_template" pyproject.toml && ! grep -q "\${PROJECT_NAME}" pyproject.toml; then
    warning "This project appears to already be initialized (no placeholders found)."
    echo "Do you want to continue anyway? This might overwrite existing files. (y/N)"
    read -r response
    if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        info "Bootstrap cancelled. No changes were made."
        exit 0
    fi
    warning "Proceeding with initialization anyway..."
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    info "Creating virtual environment..."
    uv venv
    info "Virtual environment created at .venv/"
fi

# Activate virtual environment
info "Activating virtual environment..."
source .venv/bin/activate || {
    error "Failed to activate virtual environment."
    exit 1
}

# Install poethepoet
info "Installing poethepoet..."
uv pip install poethepoet

# Try to initialize the project
info "Initializing project as: $PROJECT_NAME"

# Ensure the init_project.py script exists
if [ ! -f "scripts/init_project.py" ]; then
    error "Initialization script not found at scripts/init_project.py"
    exit 1
fi

# Run the initialization script (but don't exit on error)
set +e
python scripts/init_project.py "$PROJECT_NAME"
INIT_RESULT=$?
set -e

# Check if initialization succeeded
if [ $INIT_RESULT -ne 0 ]; then
    warning "The initialization script reported an error."
    warning "It might be that the project is already initialized."
    echo "Do you want to continue with dependency installation anyway? (Y/n)"
    read -r response
    if [[ "$response" =~ ^([nN][oO]|[nN])$ ]]; then
        info "Bootstrap cancelled."
        exit 0
    fi
    info "Continuing with setup..."
fi

# Install dependencies and setup
info "Installing dependencies and setting up project..."
uv pip install -e .[dev]

# Run format and check
info "Formatting code and running type checks..."
uv run poe format
uv run poe check

echo ""
success "Project successfully bootstrapped as: $PROJECT_NAME"
echo "You can now run tasks with: uv run poe <task-name>"
echo ""
info "Available tasks:"
uv run poe --help
