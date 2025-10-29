"""Configuration management for the SDK."""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class SDKConfig:
    """Configuration for the Value SDK."""

    secret: str
    otel_endpoint: str = "http://localhost:4317"
    backend_url: Optional[str] = None
    service_name: str = "value-control-agent"
    enable_console_export: bool = False

    def __post_init__(self) -> None:
        if not self.secret:
            raise ValueError("Agent secret is required")


def load_config_from_env() -> SDKConfig:
    """Load SDK configuration from environment variables."""
    return SDKConfig(
        secret=os.getenv("VALUE_AGENT_SECRET", ""),
        otel_endpoint=os.getenv("VALUE_OTEL_ENDPOINT", "http://localhost:4317"),
        backend_url=os.getenv("VALUE_BACKEND_URL"),
        service_name=os.getenv("VALUE_SERVICE_NAME", "value-control-agent"),
        enable_console_export=os.getenv("VALUE_CONSOLE_EXPORT", "false").lower() == "true",
    )
