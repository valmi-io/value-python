# Value Control SDK

OpenTelemetry-based SDK for agent observability and control.

## Features

- **Auto-instrumentation**: Automatic tracing for LangChain and Gemini APIs
- **Custom Actions**: Send custom events and actions as OpenTelemetry spans
- **Agent Context**: Automatic enrichment with org/workspace metadata
- **OpenTelemetry Native**: Built on industry-standard observability
- **Async First**: Built for modern async Python applications

## Installation

```bash
# Install with Poetry
poetry add value-control-sdk

# Or with pip
pip install value-control-sdk

# With optional instrumentation libraries
poetry add value-control-sdk -E instrumentation
```

## Quick Start

```python
import asyncio
from value import AsyncValueSDK, autoinstrument, agent_context

# Initialize SDK
sdk = AsyncValueSDK()

# Enable auto-instrumentation
autoinstrument(libraries=["langchain", "gemini"])

# Use agent context decorator
@agent_context(agent_task_name="agetn-task-name")
async def process_query(query: str):
    # Create custom action
    with sdk.actions.start("summarize", {"query": query}) as span:
        span.add_event("Processing started")
        # Your agent logic here
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
