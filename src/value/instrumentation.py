"""Auto-instrumentation for supported libraries."""

from typing import List, Optional
import warnings


SUPPORTED_LIBRARIES = {
    "langchain": "opentelemetry.instrumentation.langchain.LangChainInstrumentor",
    "gemini": "opentelemetry.instrumentation.google_generativeai.GoogleGenerativeAiInstrumentor",
}


def auto_instrument(libraries: Optional[List[str]] = None) -> None:
    """
    Enable auto-instrumentation for supported libraries.

    Args:
        libraries: List of library names to instrument (e.g., ["langchain", "gemini"]).
                  If None, instruments all supported libraries.

    Raises:
        ImportError: If a required instrumentation package is not installed.
    """
    if libraries is None:
        libraries_to_instrument = list(SUPPORTED_LIBRARIES.keys())
    else:
        libraries_to_instrument = libraries

    for lib in libraries_to_instrument:
        if lib not in SUPPORTED_LIBRARIES:
            warnings.warn(
                f"Instrumentation for '{lib}' is not supported. "
                f"Supported libraries: {list(SUPPORTED_LIBRARIES.keys())}"
            )
            continue

        try:
            # Dynamically import the instrumentor class
            module_path, class_name = SUPPORTED_LIBRARIES[lib].rsplit(".", 1)
            module = __import__(module_path, fromlist=[class_name])
            instrumentor_class = getattr(module, class_name)

            # Instrument the library
            instrumentor_class().instrument()

        except ImportError as e:
            raise ImportError(
                f"Could not import instrumentor for '{lib}'. "
                f"Install it with: poetry add value-control-sdk -E instrumentation\n"
                f"Error: {e}"
            )
        except Exception as e:
            warnings.warn(f"Failed to instrument {lib}: {e}")
