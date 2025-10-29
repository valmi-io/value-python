"""Tests for the SDK client."""

import pytest
from value import AsyncValueSDK, ValueSDK


def test_async_sdk_initialization() -> None:
    """Test async SDK client initialization."""
    sdk = AsyncValueSDK(secret="test-secret")
    assert sdk.secret == "test-secret"
    assert sdk.actions is not None
    assert sdk.tracer is not None


def test_sync_sdk_initialization() -> None:
    """Test sync SDK client initialization."""
    sdk = ValueSDK(secret="test-secret")
    assert sdk.secret == "test-secret"
    assert sdk.actions is not None
    assert sdk.tracer is not None


def test_sdk_requires_secret() -> None:
    """Test that SDK requires a secret."""
    with pytest.raises(ValueError, match="Agent secret must be provided"):
        AsyncValueSDK(secret="")


def test_custom_endpoints() -> None:
    """Test SDK with custom endpoints."""
    sdk = AsyncValueSDK(
        secret="test-secret",
        otel_endpoint="http://custom:4317",
        backend_url="https://custom-backend.com",
    )
    assert sdk._otel_endpoint == "http://custom:4317"
    assert sdk.api_client.base_url == "https://custom-backend.com"


@pytest.mark.asyncio
async def test_action_emitter() -> None:
    """Test custom action creation."""
    sdk = AsyncValueSDK(secret="test-secret")

    with sdk.actions.start("test_action", {"test_attr": "value"}) as span:
        span.add_event("Test event")
        assert span.is_recording()
