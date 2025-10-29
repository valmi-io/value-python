"""Tests for decorators."""

import pytest
from value import agent_context


@pytest.mark.asyncio
async def test_async_agent_context_decorator() -> None:
    """Test async agent context decorator."""

    @agent_context()
    async def test_function() -> str:
        return "test result"

    result = await test_function()
    assert result == "test result"


def test_sync_agent_context_decorator() -> None:
    """Test sync agent context decorator."""

    @agent_context()
    def test_function() -> str:
        return "test result"

    result = test_function()
    assert result == "test result"


@pytest.mark.asyncio
async def test_agent_context_with_exception() -> None:
    """Test agent context decorator handles exceptions."""

    @agent_context()
    async def test_function() -> None:
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        await test_function()
