"""Tests for instrumentation."""

import pytest
from value.instrumentation import autoinstrument


def test_autoinstrument_unsupported_library() -> None:
    """Test that unsupported libraries raise warnings."""
    with pytest.warns(UserWarning, match="not supported"):
        autoinstrument(libraries=["unsupported_lib"])
