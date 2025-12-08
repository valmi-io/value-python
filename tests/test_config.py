"""Tests for configuration."""

import pytest

from value.internal.config import SDKConfig


def test_config_requires_secret() -> None:
    """Test that config requires a secret."""
    with pytest.raises(ValueError, match="Agent secret is required"):
        SDKConfig(secret="")


def test_config_with_defaults() -> None:
    """Test config with default values."""
    config = SDKConfig(secret="test-secret")
    assert config.secret == "test-secret"
    assert config.otel_endpoint == "http://localhost:4317"
    assert config.service_name == "value-control-agent"
    assert config.enable_console_export is False
