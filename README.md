# SDK Configuration

The client can be configured using the following environment variables:

- _VALUE_AGENT_SECRET_: Agent authentication secret (required)
- _VALUE_OTEL_ENDPOINT_: OpenTelemetry collector endpoint (default: http://localhost:4317)
- _VALUE_BACKEND_URL_: Value Control Plane backend URL (required)
- _VALUE_SERVICE_NAME_: Service name for OpenTelemetry resource (default: value-control-agent)
- _VALUE_CONSOLE_EXPORT_: Enable console span exporter for debugging ("true" to enable)

# Value Control SDK

OpenTelemetry-based client for agent observability and control.

```python
# Asynchronous workflow
import asyncio
from value import initialize_async

async def main():
    client = await initialize_async()

    async def process_data(data: str) -> str:
        print(f"Processing data: {data}")
        await asyncio.sleep(0.5)
        result = data.upper()
        client.actions.send(
            "transform_data",
            {"value.action.description": f"Transformed data from {len(data)} to {len(result)} characters"}
        )
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
