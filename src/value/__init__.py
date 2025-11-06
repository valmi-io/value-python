"""Value Control SDK for OpenTelemetry-based agent observability."""

from .client import AsyncValueClient, ValueClient, initialize_async, initialize_sync
from .instrumentation import auto_instrument

__version__ = "0.1.0"
__all__ = [
    "ValueClient",
    "AsyncValueClient",
    "auto_instrument",
    "initialize_async",
    "initialize_sync",
]
