"""Async example demonstrating the Value SDK usage."""

from dotenv import load_dotenv
import os

load_dotenv()

import asyncio
from value import AsyncValueSDK, agent_context


async def main() -> None:
    # Initialize SDK (async version)
    sdk = AsyncValueSDK()
    await sdk.initialize()

    # Define agent workflow with context
    @agent_context(agent_task_name="async-agent")
    async def process_data(data: str) -> str:
        """Process data with tracing."""
        print(f"Processing data: {data}")

        # Create a custom action
        with sdk.actions.start(
            action_name="transform_data",
            attributes={"data_length": len(data)},
        ) as action_span:
            # Add events
            action_span.add_event("Starting transformation")

            # Process data
            await asyncio.sleep(0.5)
            result = data.upper()

            # Add result attributes
            action_span.set_attribute("result_length", len(result))
            action_span.add_event("Transformation complete")

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
