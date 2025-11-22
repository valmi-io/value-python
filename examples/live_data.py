"""
Live data simulation script for Value SDK.
Simulates a pipeline of events running every 5 seconds:
1. Object detection
2. Object classification
3. OCR
4. RAG
5. LLM call (Ollama or Gemini)
"""

import asyncio
import random
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

from value import initialize_async
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

# Synthetic data generators
INVOICE_TYPES = ["invoice", "receipt", "bill", "purchase_order"]
VENDORS = ["Amazon", "Google", "Microsoft", "Apple", "Uber", "Lyft", "Walmart", "Target"]
ITEMS = ["Laptop", "Monitor", "Keyboard", "Mouse", "Desk", "Chair", "Headphones"]
CURRENCIES = ["USD", "EUR", "GBP", "CAD"]

def generate_trace_id() -> str:
    return hex(random.getrandbits(128))[2:].zfill(32)

def generate_span_id() -> str:
    return hex(random.getrandbits(64))[2:].zfill(16)

async def simulate_delay():
    """Wait for 1 to 2 seconds randomly."""
    delay = random.uniform(1.0, 2.0)
    await asyncio.sleep(delay)
    return delay

class PipelineSimulator:
    def __init__(self, client):
        self.client = client
        self.tracer = client.tracer

    async def run_pipeline(self):
        """Run a single iteration of the pipeline."""
        user_id = f"user_{random.randint(1000, 9999)}"
        anonymous_id = str(uuid.uuid4())
        invoice_id = f"INV-{random.randint(10000, 99999)}"
        
        print(f"\n--- Starting pipeline for {invoice_id} (User: {user_id}) ---")

        # 1. Object Detection
        await self._step_object_detection(user_id, anonymous_id, invoice_id)

        # 2. Object Classification
        await self._step_object_classification(user_id, anonymous_id, invoice_id)

        # 3. OCR
        detected_text = await self._step_ocr(user_id, anonymous_id, invoice_id)

        # 4. RAG
        context = await self._step_rag(user_id, anonymous_id, invoice_id, detected_text)

        # 5. LLM Call
        await self._step_llm(user_id, anonymous_id, invoice_id, context)

    async def _step_object_detection(self, user_id: str, anonymous_id: str, invoice_id: str):
        print("1. Running Object Detection...")
        await simulate_delay()
        
        confidence = random.uniform(0.85, 0.99)
        box_count = random.randint(3, 10)
        
        with self.client.action_span(anonymous_id=anonymous_id, user_id=user_id) as span:
            span.send(
                action_name="object_detection",
                **{
                    "value.action.description": f"Detected {box_count} objects in {invoice_id}",
                    "invoice_id": invoice_id,
                    "model": "yolov8-invoice",
                    "confidence_score": confidence,
                    "detected_boxes": box_count,
                    "processing_device": "cuda:0"
                }
            )

    async def _step_object_classification(self, user_id: str, anonymous_id: str, invoice_id: str):
        print("2. Running Object Classification...")
        await simulate_delay()
        
        doc_type = random.choice(INVOICE_TYPES)
        confidence = random.uniform(0.90, 0.99)
        
        with self.client.action_span(anonymous_id=anonymous_id, user_id=user_id) as span:
            span.send(
                action_name="object_classification",
                **{
                    "value.action.description": f"Classified document as {doc_type}",
                    "invoice_id": invoice_id,
                    "document_type": doc_type,
                    "classification_confidence": confidence,
                    "model": "resnet50-finetuned"
                }
            )

    async def _step_ocr(self, user_id: str, anonymous_id: str, invoice_id: str) -> str:
        print("3. Running OCR...")
        await simulate_delay()
        
        vendor = random.choice(VENDORS)
        total = round(random.uniform(10.0, 500.0), 2)
        currency = random.choice(CURRENCIES)
        date = datetime.now().strftime("%Y-%m-%d")
        
        detected_text = f"Invoice from {vendor}\nDate: {date}\nTotal: {total} {currency}"
        
        with self.client.action_span(anonymous_id=anonymous_id, user_id=user_id) as span:
            span.send(
                action_name="ocr_processing",
                **{
                    "value.action.description": f"Extracted text from {invoice_id}",
                    "invoice_id": invoice_id,
                    "ocr_engine": "tesseract",
                    "language": "eng",
                    "text_length": len(detected_text),
                    "confidence": random.uniform(0.8, 0.95)
                }
            )
        return detected_text

    async def _step_rag(self, user_id: str, anonymous_id: str, invoice_id: str, query_text: str) -> str:
        print("4. Running RAG...")
        await simulate_delay()
        
        chunks_retrieved = random.randint(2, 5)
        
        with self.client.action_span(anonymous_id=anonymous_id, user_id=user_id) as span:
            span.send(
                action_name="rag_retrieval",
                **{
                    "value.action.description": f"Retrieved {chunks_retrieved} chunks for context",
                    "invoice_id": invoice_id,
                    "vector_db": "chroma",
                    "embedding_model": "text-embedding-3-small",
                    "chunks_count": chunks_retrieved,
                    "top_k": 5
                }
            )
        return f"Context for {query_text}"

    async def _step_llm(self, user_id: str, anonymous_id: str, invoice_id: str, context: str):
        print("5. Running LLM Call...")
        delay = await simulate_delay()
        
        is_gemini = random.choice([True, False])
        
        if is_gemini:
            await self._simulate_gemini_call(user_id, anonymous_id, invoice_id, delay)
        else:
            await self._simulate_ollama_call(user_id, anonymous_id, invoice_id, delay)

    async def _simulate_gemini_call(self, user_id: str, anonymous_id: str, invoice_id: str, duration: float):
        print("   -> Simulating Gemini API Call")
        
        model = "gemini-2.5-flash"
        prompt = f"Summarize invoice {invoice_id}"
        response_text = f"This is a summary of invoice {invoice_id} from Gemini."
        
        # Manually create a span that looks like the Gemini auto-instrumented span
        tracer = self.client.tracer
        start_time = time.time_ns()
        end_time = start_time + int(duration * 1e9)
        
        attributes = {
            "gen_ai.system": "Google",
            "llm.request.type": "completion",
            "value.action.user_id": user_id,
            "value.action.anonymous_id": anonymous_id,
            "gen_ai.prompt.0.content": f"[{{\"type\": \"text\", \"text\": \"{prompt}\"}}]",
            "gen_ai.prompt.0.role": "user",
            "gen_ai.request.model": model,
            "gen_ai.completion.0.content": response_text,
            "gen_ai.completion.0.role": "assistant",
            "gen_ai.response.model": model,
            "llm.usage.total_tokens": random.randint(100, 1000),
            "gen_ai.usage.completion_tokens": random.randint(50, 200),
            "gen_ai.usage.prompt_tokens": random.randint(10, 50)
        }
        
        span = tracer.start_span(
            name="gemini.generate_content",
            kind=trace.SpanKind.CLIENT,
            attributes=attributes,
            start_time=start_time
        )
        span.end(end_time=end_time)
        
        # Also send the value.action span for processing the response
        with self.client.action_span(anonymous_id=anonymous_id, user_id=user_id) as action_span:
            action_span.send(
                action_name="process_gemini_response",
                **{
                    "value.action.description": f"Received response from {model}",
                    "custom.model": model,
                    "custom.response_length": len(response_text),
                    "custom.prompt_type": "summarization"
                }
            )

    async def _simulate_ollama_call(self, user_id: str, anonymous_id: str, invoice_id: str, duration: float):
        print("   -> Simulating Ollama API Call")
        
        model = "llama3"
        prompt = f"Extract details from {invoice_id}"
        response_text = f"Extracted details for {invoice_id} using Ollama."
        
        # Manually create a span for Ollama
        tracer = self.client.tracer
        start_time = time.time_ns()
        end_time = start_time + int(duration * 1e9)
        
        attributes = {
            "value.action.llm.model": model,
            "value.action.llm.input_tokens": random.randint(10, 50),
            "value.action.llm.output_tokens": random.randint(50, 200),
            "value.action.llm.total_tokens": random.randint(100, 1000),
            "value.action.llm.prompt": prompt,
            "value.action.llm.response": response_text,
        }
        
        span = tracer.start_span(
            name="ollama.generate",
            kind=trace.SpanKind.CLIENT,
            attributes=attributes,
            start_time=start_time
        )
        span.end(end_time=end_time)
        
        # Also send the value.action span
        with self.client.action_span(anonymous_id=anonymous_id, user_id=user_id) as action_span:
            action_span.send(
                action_name="process_ollama_response",
                **{
                    "value.action.description": f"Received response from {model}",
                    "custom.model": model,
                    "custom.response_length": len(response_text),
                    "custom.prompt_type": "extraction"
                }
            )

async def main():
    print("Initializing Value SDK...")
    client = await initialize_async()
    simulator = PipelineSimulator(client)
    
    print("Starting Live Data Simulation (Ctrl+C to stop)...")
    try:
        while True:
            await simulator.run_pipeline()
            print("Waiting 5 seconds for next iteration...")
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    asyncio.run(main())
