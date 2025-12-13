import os
from dotenv import load_dotenv

load_dotenv()

from value.instrumentation import auto_instrument
from value import initialize_sync
from google import genai

# Get agent secret from environment variable
AGENT_SECRET = os.getenv("VALUE_AGENT_SECRET", "your-agent-secret")

value_client = initialize_sync(agent_secret=AGENT_SECRET)
auto_instrument(["gemini"])

api_key = os.getenv("GOOGLE_API_KEY", "your-gemini-api-key-here")
print(api_key)

gemini_client = genai.Client(api_key=api_key)
model = 'gemini-2.5-flash'
prompt = "Write a short, fun poem about tracing."

print(f"\nMaking call to {model}...")

try:
    with value_client.action_context(user_id="user123", anonymous_id="anon456") as ctx:
        response = gemini_client.models.generate_content(model=model, contents=[prompt])

        ctx.send(
            action_name="process_gemini_response",
            **{
                "value.action.description": f"Received response from {model} with {len(response.text)} characters",
                "custom.model": model,
                "custom.response_length": len(response.text),
                "custom.prompt_type": "creative_writing",
            },
        )

        print("\n--- Gemini Response ---")
        print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")

print("\nTracing Complete. Check the console output for the generated spans.")
