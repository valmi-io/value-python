"""Action emitter for creating custom OpenTelemetry spans."""

from typing import Optional, Dict, Any
from contextlib import contextmanager
from opentelemetry import trace


class ActionEmitter:
    """Emitter for creating custom actions (OpenTelemetry spans)."""

    def __init__(self, tracer: trace.Tracer):
        """
        Initialize the action emitter.

        Args:
            tracer: OpenTelemetry tracer instance
        """
        self._tracer = tracer

    @contextmanager
    def start(self, action_name: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Start a new action as an OpenTelemetry span. Use as a context manager.

        Automatically enriches span with organization_id, workspace_id, and agent_name if available.

        Args:
            action_name: Name of the action
            attributes: Optional dict of attributes to attach to the span

        Yields:
            The active span object
        """
        enriched_attributes = dict(attributes or {})
        with self._tracer.start_as_current_span(name=action_name, attributes=enriched_attributes) as span:
            yield span
