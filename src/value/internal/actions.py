"""Action emitter for creating custom OpenTelemetry spans."""

import warnings
from typing import Optional, Dict, Any
from contextlib import contextmanager
from opentelemetry import trace
from .config import ALLOWED_ACTION_ATTRIBUTES


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
        
        # Check for non-standard attributes
        non_standard_attrs = [
            key for key in enriched_attributes.keys()
            if key not in ALLOWED_ACTION_ATTRIBUTES
        ]
        
        if non_standard_attrs:
            warnings.warn(
                "Warning: Non-standard attributes were provided. These attributes will be ignored and will not appear in the final traces"
            )
            # Filter out non-standard attributes
            enriched_attributes = {
                key: value for key, value in enriched_attributes.items()
                if key in ALLOWED_ACTION_ATTRIBUTES
            }
        
        enriched_attributes["value.action.name"] = action_name
        with self._tracer.start_as_current_span(name="value.action", attributes=enriched_attributes):
            # Span is automatically ended when exiting the context, which sends it
            pass

