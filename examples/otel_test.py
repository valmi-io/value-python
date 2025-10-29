from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Create a resource to identify your service
resource = Resource(attributes={"service.name": "my-python-service"})

# Set up the tracer provider
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer_provider = trace.get_tracer_provider()

# Configure OTLP exporter to send to collector via HTTP
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",  # HTTP endpoint (note: 4318, not 4317)
)

# Add the exporter to the tracer provider
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Get a tracer
tracer = trace.get_tracer(__name__)


# Create and send some example traces
def main():
    # Start a parent span
    with tracer.start_as_current_span("parent-operation") as parent_span:
        parent_span.set_attribute("user.id", "123")
        parent_span.set_attribute("operation.type", "example")

        print("Sending parent span...")

        # Create a child span
        with tracer.start_as_current_span("child-operation") as child_span:
            child_span.set_attribute("step", "processing")
            print("Sending child span...")

            # Simulate some work
            import time

            time.sleep(0.1)

        # Another child span
        with tracer.start_as_current_span("another-child-operation") as child_span:
            child_span.set_attribute("step", "finalizing")
            print("Sending another child span...")
            time.sleep(0.05)

    print("Traces sent successfully!")

    # Force flush to ensure all spans are sent
    tracer_provider.force_flush()


if __name__ == "__main__":
    main()
