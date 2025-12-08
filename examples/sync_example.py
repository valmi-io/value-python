"""Synchronous example demonstrating the Value SDK usage."""

from dotenv import load_dotenv
import os

load_dotenv()

import time
from value import initialize_sync


def main() -> None:
    client = initialize_sync()

    def process_data(data: str) -> str:
        """Process data with tracing."""
        print(f"Processing data: {data}")

        result = data.upper()

        with client.action_context(user_id="user123", anonymous_id="anon456") as ctx:
            ctx.send(
                action_name="transform_data",
                **{
                    "value.action.description": f"Transformed data from {len(data)} to {len(result)} characters",
                    "original_text": data,
                    "transformed_text": result,
                    "method": "uppercase",
                    "is_cached": False,
                },
            )

        return result

    result = process_data("hello world")
    print(f"Result: {result}")

    time.sleep(2)


if __name__ == "__main__":
    print("=" * 50)
    print("Value SDK Sync Example")
    print("=" * 50)
    print("\nNote: Make sure you have an OpenTelemetry collector running:")
    print("  docker run -p 4317:4317 otel/opentelemetry-collector:latest\n")

    main()
