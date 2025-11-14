"""Async example demonstrating the Value SDK usage with Direct send action without start / add_events."""

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

        # Send action with name and parameters (simplified API)
        client.actions.send(
            action_name="transform_data",
            attributes={
                "data_length": len(data),
                "result_length": len(result),
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
    print("Value SDK Async Example (Simplified)")
    print("=" * 50)
    print("\nThis example uses the simplified send() API:")
    print("  client.actions.send(action_name, attributes)")
    print("\nNote: Make sure you have an OpenTelemetry collector running:")
    print("  docker run -p 4317:4317 otel/opentelemetry-collector:latest\n")

    asyncio.run(main())

