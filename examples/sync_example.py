"""Synchronous example demonstrating the Value SDK usage."""

from dotenv import load_dotenv
import os

load_dotenv()

import time
from value import initialize_sync


def main() -> None:
    # Initialize SDK (sync version)
    client = initialize_sync()

    # Define agent workflow
    def process_data(data: str) -> str:
        """Process data with tracing."""
        print(f"Processing data: {data}")

        # Create a custom action
        with client.actions.start(
            action_name="transform_data",
            attributes={"data_length": len(data)},
        ) as action_span:
            # Add events
            action_span.add_event("Starting transformation")

            # Process data
            result = data.upper()

            # Add result attributes
            action_span.set_attribute("result_length", len(result))
            action_span.add_event("Transformation complete")

        return result

    # Run the workflow
    result = process_data("hello world")
    print(f"Result: {result}")

    # Allow time for spans to be exported
    time.sleep(2)


if __name__ == "__main__":
    print("=" * 50)
    print("Value SDK Sync Example")
    print("=" * 50)
    print("\nNote: Make sure you have an OpenTelemetry collector running:")
    print("  docker run -p 4317:4317 otel/opentelemetry-collector:latest\n")

    main()
