"""Value Control SDK for OpenTelemetry-based agent observability."""

from .client import AsyncValueSDK, ValueSDK, initialize_sdk_async, initialize_sdk_sync
from .decorators import agent_context
from .instrumentation import auto_instrument

__version__ = "0.1.0"
__all__ = [
    "ValueSDK",
    "AsyncValueSDK",
    "agent_context",
    "auto_instrument",
    "initialize_sdk_async",
    "initialize_sdk_sync",
]
