"""Tests for the SDK client."""

import pytest
from value import AsyncValueClient, ValueClient


@pytest.mark.asyncio
async def test_async_sdk_initialization() -> None:
    """Test async SDK client initialization."""
    sdk = AsyncValueClient(secret="test-secret")
    assert sdk.secret == "test-secret"
    await sdk.initialize()
    assert sdk.actions_emitter is not None
    assert sdk.tracer is not None


def test_sync_sdk_initialization() -> None:
    """Test sync SDK client initialization."""
    sdk = ValueClient(secret="test-secret")
    assert sdk.secret == "test-secret"
    sdk.initialize()
    assert sdk.actions_emitter is not None
    assert sdk.tracer is not None


def test_sdk_requires_secret() -> None:
    """Test that SDK requires a secret."""
    with pytest.raises(ValueError, match="Agent secret must be provided"):
        AsyncValueClient(secret="")


def test_custom_endpoints() -> None:
    """Test SDK with custom endpoints."""
    sdk = AsyncValueClient(
        secret="test-secret",
        otel_endpoint="http://custom:4317",
        backend_url="https://custom-backend.com",
    )
    assert sdk._otel_endpoint == "http://custom:4317"
    assert sdk.api_client.base_url == "https://custom-backend.com"


@pytest.mark.asyncio
async def test_action_emitter() -> None:
    """Test custom action creation."""
    sdk = AsyncValueClient(secret="test-secret")
    await sdk.initialize()

    # Test sending action without context
    sdk.action().send(
        action_name="test_action",
        user_id="user123",
        anonymous_id="anon456",
        **{"value.action.description": "Test action"}
    )

    # Test sending action within context
    with sdk.action_span(user_id="user123", anonymous_id="anon456") as action_span:
        action_span.send(action_name="test_action_2", **{"value.action.description": "Test action 2"})
