from dotenv import load_dotenv
import os

# Dummy tool for demonstration

# Load environment variables from .env file
load_dotenv()
"""
Agentic workflow example using LangChain to test auto-instrumentation and action traces.
"""

from value.instrumentation import autoinstrument
from value import ValueSDK

from google import genai


# Dummy tool for demonstration


# Setup ValueSDK for context enrichment
sdk = ValueSDK()
sdk.initialize()


# Auto-instrumentation setup
autoinstrument(["gemini"])

api_key = os.getenv("GOOGLE_API_KEY", "your-gemini-api-key-here")
print(api_key)

client = genai.Client(api_key=api_key)
model = 'gemini-2.5-flash'
prompt = "Write a short, fun poem about tracing."

print(f"\n🚀 Making call to {model}...")

try:
    # The call is now automatically instrumented! No manual span creation needed.
    response = client.models.generate_content(model=model, contents=[prompt])

    print("\n--- Gemini Response ---")
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")

# The BatchSpanProcessor will flush pending spans when the program exits.
print("\n✨ Tracing Complete. Check the console output for the generated spans.")
