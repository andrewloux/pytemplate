"""
Utility functions for the application.
"""
import os
from pathlib import Path
from typing import TextIO, Optional, Final, cast


# Use Final for constants
DEFAULT_ENCODING: Final[str] = "utf-8"


def get_project_root() -> Path:
    """
    Get the absolute path to the project root directory.
    
    Returns:
        Path: The project root directory path
    """
    current: Path = Path(__file__).resolve().parent.parent.parent
    
    # Look for known project markers
    if (current / "src").is_dir():
        return current
    
    # Fallback to current working directory
    return Path.cwd()


def open_resource(file_name: str, mode: str = "r", encoding: str = DEFAULT_ENCODING) -> TextIO:
    """
    Open a file from the resources directory.
    
    Args:
        file_name: Name of the resource file
        mode: File open mode
        encoding: File encoding
        
    Returns:
        TextIO: The opened file object
        
    Raises:
        FileNotFoundError: If the resource file doesn't exist
    """
    resource_path: Path = get_project_root() / "resources" / file_name
    
    if not resource_path.exists():
        raise FileNotFoundError(f"Resource not found: {file_name}")
    
    return cast(TextIO, resource_path.open(mode=mode, encoding=encoding))


def get_env_var(name: str, default: Optional[str] = None) -> str:
    """
    Get an environment variable with validation.
    
    Args:
        name: Name of the environment variable
        default: Default value if not set
        
    Returns:
        str: Value of the environment variable
        
    Raises:
        ValueError: If the variable is not set and no default is provided
    """
    value: Optional[str] = os.environ.get(name, default)
    
    if value is None:
        raise ValueError(f"Environment variable {name} is not set and no default provided")
    
    return value