"""Decorators for automatic context enrichment."""

import functools
import asyncio
import contextvars

from opentelemetry import trace
from typing import Callable, Any

# Context variable for agent task name
agent_task_name_var = contextvars.ContextVar("agent_task_name", default=None)


def agent_context(agent_task_name: str = "unknown") -> Callable:
    """
    Decorator that enriches spans with agent context from the backend.

    Args:
        agent_name: Name of the agent to use as context

    Example:
        @agent_context(agent_task_name="my-agent")
        async def my_agent_function():
            # Context automatically added to all spans in this function
            pass
    """

    def decorator(func: Callable) -> Callable:
        # Handle async functions
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                token = agent_task_name_var.set(agent_task_name)
                current_span = trace.get_current_span()
                if current_span.is_recording():
                    try:
                        current_span.set_attributes({"value.agent.task.name": agent_task_name})
                    except Exception as e:
                        current_span.set_attribute("agent.context_error", str(e))
                        current_span.record_exception(e)
                try:
                    return await func(*args, **kwargs)
                finally:
                    agent_task_name_var.reset(token)

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                token = agent_task_name_var.set(agent_task_name)
                current_span = trace.get_current_span()
                if current_span.is_recording():
                    try:
                        current_span.set_attributes({"value.agent.task.name": agent_task_name})
                    except Exception as e:
                        current_span.set_attribute("agent.context_error", str(e))
                        current_span.record_exception(e)
                try:
                    return func(*args, **kwargs)
                finally:
                    agent_task_name_var.reset(token)

            return sync_wrapper

    return decorator
