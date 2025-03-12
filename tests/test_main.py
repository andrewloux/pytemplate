"""
Tests for main module.
"""
from typing import Dict, Any

import pytest
from unittest.mock import patch, MagicMock

from src.main import get_config, configure_logging, AppConfig


def test_get_config() -> None:
    """Test get_config returns the correct configuration."""
    config: AppConfig = get_config()

    assert isinstance(config, dict)
    assert "name" in config
    assert "debug" in config
    assert "version" in config
    assert isinstance(config["debug"], bool)


@patch("builtins.print")
def test_configure_logging(mock_print: MagicMock) -> None:
    """Test configure_logging function."""
    # Test with default level
    configure_logging()
    mock_print.assert_called_once()
    assert "INFO" in mock_print.call_args[0][0]

    # Reset mock
    mock_print.reset_mock()

    # Test with custom level
    configure_logging(level="ERROR")
    mock_print.assert_called_once()
    assert "ERROR" in mock_print.call_args[0][0]
