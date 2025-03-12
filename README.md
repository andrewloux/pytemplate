# ${PROJECT_NAME}

A modern, strongly-typed Python project using uv and poethepoet.

## Features

- **Ultra-Fast Dependency Management**: Using uv, the next-generation Python package manager
- **Modern Task Runner**: Task automation with poethepoet
- **Comprehensive Type Safety**: Ultra-strict type checking with mypy
- **Modern Type Annotations**: TypedDict, Literal, and Final type annotations
- **Testing Framework**: pytest with coverage reporting
- **Code Formatting**: Black code formatter
- **Data Validation**: Pydantic for runtime validation
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

2. Run the initialization script with your project name:
   ```bash
   # Initialize project (project name must be lowercase with underscores)
   ./scripts/init.sh my_project_name
   ```

3. Complete setup with a single command:
   ```bash
   # Install dependencies, format code, and verify type checking
   uv pip install -e .[dev] && uv run poe setup
   ```

That's it! Your project is now ready for development.

## Task Runner (uv + poe)

This template uses uv for dependency management and poethepoet (poe) for task running:

```bash
# Run any task with:
uv run poe <task-name>
```

### Available Tasks

| Task      | Description                                   | Command                |
|-----------|-----------------------------------------------|------------------------|
| init      | Install with regular dependencies             | uv run poe init        |
| devinit   | Install with development dependencies         | uv run poe devinit     |
| format    | Format code with black                        | uv run poe format      |
| check     | Type check with mypy                          | uv run poe check       |
| test      | Run tests with pytest                         | uv run poe test        |
| test-cov  | Run tests with coverage                       | uv run poe test-cov    |
| setup     | Full dev setup (installs, formats, checks)    | uv run poe setup       |

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
uv run poe devinit

# 2. Create a new branch
git checkout -b feature/my-feature

# 3. Make your changes...

# 4. Format and type check
uv run poe format
uv run poe check

# 5. Run tests
uv run poe test

# 6. Commit your changes
git add .
git commit -m "Add my feature"
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

- Add a new dependency: `uv add package_name`
- Remove a dependency: `uv remove package_name`
- Update dependencies: `uv pip install -U -e .[dev]`

## CI/CD Integration

This template is ready for CI integration with GitHub Actions or similar services. See the included workflow files for details.
