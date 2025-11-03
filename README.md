# SDK Configuration

The SDK can be configured using the following environment variables:

- _VALUE_AGENT_SECRET_: Agent authentication secret (required)
- _VALUE_OTEL_ENDPOINT_: OpenTelemetry collector endpoint (default: http://localhost:4317)
- _VALUE_BACKEND_URL_: Value Control Plane backend URL (required)
- _VALUE_SERVICE_NAME_: Service name for OpenTelemetry resource (default: value-control-agent)
- _VALUE_CONSOLE_EXPORT_: Enable console span exporter for debugging ("true" to enable)

# Value Control SDK

OpenTelemetry-based SDK for agent observability and control.

```python
# Asynchronous workflow
import asyncio
from value import initialize_sdk_async, agent_context

async def main():
    sdk = await initialize_sdk_async()

    @agent_context(agent_task_name="async-task")
    async def process_data(data: str) -> str:
        print(f"Processing data: {data}")
        with sdk.actions.start("transform_data", {"data_length": len(data)}) as span:
            span.add_event("Start transformation")
            await asyncio.sleep(0.5)
            result = data.upper()
            span.set_attribute("result_length", len(result))
            span.add_event("Transformation complete")
        return result

    result = await process_data("hello async world")
    print(f"Result: {result}")

asyncio.run(main())
```

# Auto instrumentation

```python
from value import auto_instrument

auto_instrument(libraries=["langchain", "gemini"])
```

# Use agent context decorator

```python

import asyncio
from value import agent_context, initialize_sdk_sync

sdk = initialize_sdk_sync()

@agent_context(agent_task_name="agent-task-name")
async def process_query(query: str): # Create custom action
    with sdk.actions.start("summarize", {"query": query}) as span:
        span.add_event("Processing started") # Your agent logic here
        result = f"Processed: {query}"
        span.add_event("Processing complete")
        return result

asyncio.run(process_query("Hello World"))

```

## Documentation

See the [examples/](examples/) directory for complete usage examples.

## Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=value --cov-report=html

# Format code
poetry run black src/ tests/

# Lint code
poetry run ruff check src/ tests/

# Type check
poetry run mypy src/
```

## License

MIT
