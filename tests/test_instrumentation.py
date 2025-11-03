"""Tests for instrumentation."""

import pytest
from value.instrumentation import auto_instrument


def test_auto_instrument_unsupported_library() -> None:
    """Test that unsupported libraries raise warnings."""
    with pytest.warns(UserWarning, match="not supported"):
        auto_instrument(libraries=["unsupported_lib"])
