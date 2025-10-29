"""Action emitter for creating custom OpenTelemetry spans."""

from typing import Optional, Dict, Any
from contextlib import contextmanager
from opentelemetry import trace

from .decorators import agent_task_name_var


class ActionEmitter:
    """Emitter for creating custom actions (OpenTelemetry spans)."""

    def __init__(self, tracer: trace.Tracer):
        """
        Initialize the action emitter.

        Args:
            tracer: OpenTelemetry tracer instance
            sdk_instance: Optional SDK instance for context enrichment
        """
        self._tracer = tracer

    @contextmanager
    def start(self, action_name: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Start a new action as an OpenTelemetry span. Use as a context manager.

        Automatically enriches span with organization_id, workspace_id, agent_name, and agent_task_name if available.

        Args:
            action_name: Name of the action
            attributes: Optional dict of attributes to attach to the span

        Yields:
            The active span object
        """
        enriched_attributes = dict(attributes or {})

        # Propagate agent_task_name from contextvars if set
        agent_task_name = agent_task_name_var.get()

        if agent_task_name:
            enriched_attributes.setdefault("value.agent.task.name", agent_task_name)
        with self._tracer.start_as_current_span(name=action_name, attributes=enriched_attributes) as span:
            yield span
