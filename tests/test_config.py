"""Tests for configuration."""

from value.internal.config import SDKConfig


def test_config_with_defaults() -> None:
    """Test config with default values."""
    config = SDKConfig(secret="test-secret")
    assert config.secret == "test-secret"
    assert config.otel_endpoint == "http://localhost:4317"
    assert config.service_name == "value-control-agent"
    assert config.enable_console_export is False


def test_config_allows_empty_secret() -> None:
    """Test that config allows empty secret (validation is done in client)."""
    config = SDKConfig(secret="")
    assert config.secret == ""
