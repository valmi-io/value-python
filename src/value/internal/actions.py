"""Action emitter for creating custom OpenTelemetry spans."""

import warnings
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

    def send(self, action_name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Send an action immediately as an OpenTelemetry span.

        Creates a span, adds attributes, and immediately ends it (sends it).

        Args:
            action_name: Name of the action
            attributes: Optional dict of attributes to attach to the span
        """
        enriched_attributes = dict(attributes or {})
        action_name_key = "value.action.name"
        if action_name_key in enriched_attributes:
            warnings.warn(
                f"Attribute key '{action_name_key}' already exists in attributes. "
                f"Its value will be replaced by the given action_name '{action_name}'."
            )
        enriched_attributes[action_name_key] = action_name
        with self._tracer.start_as_current_span(name="value.action", attributes=enriched_attributes):
            # Span is automatically ended when exiting the context, which sends it
            pass

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
        action_name_key = "value.action.name"
        if action_name_key in enriched_attributes:
            warnings.warn(
                f"Attribute key '{action_name_key}' already exists in attributes. "
                f"Its value will be replaced by the given action_name '{action_name}'."
            )
        enriched_attributes[action_name_key] = action_name
        with self._tracer.start_as_current_span(name="value.action", attributes=enriched_attributes) as span:
            yield span
