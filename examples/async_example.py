"""Async example demonstrating the Value SDK usage."""

from dotenv import load_dotenv

load_dotenv()

import asyncio
from value import initialize_async


async def main() -> None:
    # Initialize SDK (async version)
    client = await initialize_async()

    # Define agent workflow
    async def process_data(data: str) -> str:
        """Process data with tracing."""
        print(f"Processing data: {data}")

        # Process data
        await asyncio.sleep(0.5)
        result = data.upper()

        # Send a custom action with all attributes upfront
        client.actions.send(
            action_name="transform_data",
            attributes={
                "value.action.description": f"Transformed data from {len(data)} to {len(result)} characters"
            },
        )

        return result

    # Run the workflow
    result = await process_data("hello async world")
    print(f"Result: {result}")

    # Allow time for spans to be exported
    await asyncio.sleep(2)


if __name__ == "__main__":
    print("=" * 50)
    print("Value SDK Async Example")
    print("=" * 50)
    print("\nNote: Make sure you have an OpenTelemetry collector running:")
    print("  docker run -p 4317:4317 otel/opentelemetry-collector:latest\n")

    asyncio.run(main())
