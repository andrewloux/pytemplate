# ${PROJECT_NAME}

A modern, strongly-typed Python project using uv and poethepoet.

## Features

- **One-Command Bootstrap**: Get started instantly with a single command
- **Ultra-Fast Dependency Management**: Using uv, the next-generation Python package manager
- **Comprehensive Code Quality**: Integration of black (formatting), mypy (type checking), and ruff (linting)
- **Modern Task Runner**: 15+ development tasks via poethepoet for every workflow need
- **Interactive Development**: Watch mode for tests and auto-fix capabilities
- **Strict Type Checking**: Ultra-strict mypy configuration for type safety
- **Modern Type Annotations**: TypedDict, Literal, and Final type annotations
- **Testing Framework**: pytest with coverage and watch mode
- **Clean Structure**: Organized project structure with src layout

## Quick Start

1. Create a new project from this template:
   ```bash
   # Clone the template
   git clone https://github.com/username/python-project-template.git my_project
   cd my_project

   # Optional: Start fresh Git history
   rm -rf .git
   git init
   ```

2. Bootstrap the project with a single command:
   ```bash
   # Initialize, install dependencies, format code, and verify type checking
   ./bootstrap.sh my_project_name
   ```

That's it! The bootstrap script handles everything:
- Replaces project name placeholders
- Installs dependencies including development tools
- Formats code with black
- Runs type checking

### Manual Setup (Alternative)

If you prefer more control over the setup process:

1. Initialize the project:
   ```bash
   # First install poethepoet
   uv pip install poethepoet

   # Then initialize the project
   uv run poe init-project my_project_name
   ```

2. Install dependencies and set up:
   ```bash
   # Install dev dependencies
   uv pip install -e .[dev]

   # Run setup tasks
   uv run poe setup
   ```

## Task Runner (uv + poe)

This template uses uv for dependency management and poethepoet (poe) for task running:

```bash
# Run any task with:
uv run poe <task-name>
```

### Available Tasks

#### Code Quality
| Task      | Description                                   | Command                |
|-----------|-----------------------------------------------|------------------------|
| format    | Format code with black                        | uv run poe format      |
| check     | Type check with mypy                          | uv run poe check       |
| lint      | Lint code with ruff                           | uv run poe lint        |
| fix       | Auto-fix linting issues                       | uv run poe fix         |
| quality   | Run all code quality checks                   | uv run poe quality     |

#### Testing
| Task        | Description                                 | Command                   |
|-------------|---------------------------------------------|---------------------------|
| test        | Run tests with pytest                       | uv run poe test           |
| test-cov    | Run tests with coverage                     | uv run poe test-cov       |
| test-watch  | Run tests in watch mode (auto-rerun)        | uv run poe test-watch     |

#### Project Maintenance
| Task        | Description                                 | Command                   |
|-------------|---------------------------------------------|---------------------------|
| update      | Update all dependencies                     | uv run poe update         |
| list        | List installed packages                     | uv run poe list           |
| clean       | Remove all build artifacts                  | uv run poe clean          |
| build       | Build package distribution files            | uv run poe build          |

## Project Structure

```
${PROJECT_NAME}/
├── pyproject.toml    # Project metadata and dependencies
├── README.md        # Project documentation
├── .gitignore       # Git ignore patterns
├── src/             # Source code package
│   ├── ${PROJECT_NAME}/
│   │   ├── __init__.py
│   │   └── ...      # Package modules
│   └── py.typed     # Type checking marker
├── tests/           # Test directory
│   ├── __init__.py
│   └── test_*.py    # Test modules
└── resources/       # Additional resources
```

## Type Safety Guidelines

This template enforces strict typing to catch errors early:

- **Complete Type Annotations**: Every function has parameter and return annotations
- **No Implicit Any**: Disallows implicit `Any` types
- **No Partial Typing**: Disallows partial type annotations
- **Runtime Validation**: Use Pydantic for input validation
- **TypedDict**: Use for structured dictionary returns
- **Literals**: Use for string enums and constrained values
- **Final**: Mark true constants with `Final`
- **Optional**: Explicit annotation for nullable values

## Development Workflow

### Starting a New Feature

```bash
# 1. Make sure you're using the latest dependencies
uv run poe update

# 2. Create a new branch
git checkout -b feature/my-feature

# 3. Make your changes...

# 4. Run the quality checks in one go
uv run poe quality

# 5. Run tests with coverage
uv run poe test-cov

# 6. Commit your changes
git add .
git commit -m "Add my feature"
```

### Interactive Development

```bash
# Watch your tests while developing (auto-runs on file changes)
uv run poe test-watch

# Quick check between changes
uv run poe format && uv run poe fix
```

### Running Specific Tests

```bash
# Run a specific test file
uv run -- pytest tests/test_specific.py

# Run a specific test function
uv run -- pytest tests/test_file.py::test_function_name

# Run with extra verbosity
uv run -- pytest -vv tests/
```

## Dependency Management

### Installing Packages

```bash
# Install a new package and add to dependencies
uv add package_name

# Install a specific version
uv add package_name==1.2.3

# Install with extras
uv add "package_name[extra1,extra2]"

# Install a development dependency
uv add --dev pytest-mock

# Install from git
uv add git+https://github.com/user/repo.git
```

### Managing Dependencies

```bash
# List installed packages
uv run poe list

# Update all dependencies to latest compatible versions
uv run poe update

# Remove a package
uv remove package_name

# Install in development mode
uv pip install -e .

# Install with development dependencies
uv pip install -e .[dev]
```

### Managing Requirements

```bash
# Generate requirements.txt from pyproject.toml
uv pip freeze > requirements.txt

# Lock dependencies (creates requirements.lock)
uv pip freeze > requirements.lock

# Install from requirements.txt
uv pip install -r requirements.txt
```

### Best Practices

- Pin versions in production environments for reproducibility
- Use version ranges in development for flexibility
- Keep dev dependencies separate from runtime dependencies
- Regularly run `uv run poe update` to check for updates
- Consider using `uv pip compile` for more complex dependency trees

## CI/CD Integration

This template is ready for CI integration with GitHub Actions or similar services. See the included workflow files for details.
