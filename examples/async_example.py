"""Async example demonstrating the Value SDK usage."""

from dotenv import load_dotenv

load_dotenv()

import asyncio
from value import initialize_async


async def main() -> None:
    client = await initialize_async()

    async def process_data(data: str) -> str:
        """Process data with tracing."""
        print(f"Processing data: {data}")

        await asyncio.sleep(0.5)
        result = data.upper()

        with client.action_span(user_id="user123", anonymous_id="anon456") as action_span:
            action_span.send(
                action_name="transform_data",
                **{
                    "value.action.description": f"Transformed data from {len(data)} to {len(result)} characters",
                    "input_text": data,
                    "output_text": result,
                    "operation": "uppercase_transform",
                    "processing_time_ms": 500,
                },
            )

        return result

    result = await process_data("hello async world")
    print(f"Result: {result}")

    await asyncio.sleep(2)


if __name__ == "__main__":
    print("=" * 50)
    print("Value SDK Async Example")
    print("=" * 50)
    print("\nNote: Make sure you have an OpenTelemetry collector running:")
    print("  docker run -p 4317:4317 otel/opentelemetry-collector:latest\n")

    asyncio.run(main())
