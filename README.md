# PyCharm Python Project Template

This template provides a super-typed, standardized structure for Python projects in PyCharm with:

- Ultra-strict type checking with mypy
- TypedDict, Literal and Final type annotations
- Complete typing for all functions and variables
- pytest testing framework
- Black code formatting
- Consistent project structure
- Pydantic for data validation

## Setup and Usage

### Project Initialization

1. Create a new project from the template:
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
   # Initialize project with your project name (must be lowercase with underscores)
   ./scripts/init.sh my_project_name
   ```

   This script will:
   - Validate your project name
   - Recursively find and replace placeholders throughout the codebase
   - Create a virtual environment
   - Provide instructions for next steps

3. Follow the post-initialization instructions to:
   - Activate the virtual environment: `source .venv/bin/activate`
   - Install dependencies using the uv task runner

### Using UV Task Runner

Once initialized, you can use uv as a task runner:

```bash
# Install dependencies (regular)
uv run init

# Install dependencies (development)
uv run devinit

# Check types
uv run typecheck

# Format code
uv run format

# Run tests
uv run test

# Run all checks (format, typecheck, test)
uv run check
```

## Project Structure

- `src/` - Source code
  - `internal/` - Internal modules
  - `py.typed` - Marker file for typed package
- `tests/` - Test files with type annotations
- `resources/` - Data files and resources
- `mypy.ini` and `pyproject.toml` - Type checking configuration

## Type Safety Features

- No implicit Any types
- No untyped functions or parameters
- Exhaustive type checking with mypy
- Explicit Optional[T] for nullable values
- TypedDict for dictionary returns
- Literal for string enum values
- Final for true constants
- Detailed docstrings with type information

## Commands

### Development
- Type check: `mypy src/ tests/`
- Lint with black: `black src/ tests/`
- Run all tests: `pytest tests/`
- Run single test: `pytest tests/test_file.py::test_function_name`
- Run with coverage: `pytest --cov=src tests/`
