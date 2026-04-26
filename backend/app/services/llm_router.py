import time
import google.generativeai as genai
from groq import Groq
 
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)
 
MODEL_PRIORITY = [
    {"name": "Gemini 2.5 Flash",      "id": "gemini-2.5-flash",         "provider": "gemini"},
    {"name": "Groq Llama 3.3 70B",    "id": "llama-3.3-70b-versatile",  "provider": "groq"},
    {"name": "Gemini 2.5 Flash Lite", "id": "gemini-2.5-flash-lite-preview-06-17", "provider": "gemini"},
    {"name": "Groq Llama 3.1 8B",     "id": "llama-3.1-8b-instant",     "provider": "groq"},
]
 
 
def call_gemini(prompt: str, model_id: str = "gemini-2.5-flash") -> str:
    model = genai.GenerativeModel(model_id)
    response = model.generate_content(prompt)
    return response.text
 
 
def call_groq(prompt: str, model_id: str = "llama-3.3-70b-versatile") -> str:
    response = groq_client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
 
 
def call_with_fallback(prompt: str) -> str | None:
    """
    Try each model in MODEL_PRIORITY order.
    Returns the first successful response, or None if all fail.
    """
    for model in MODEL_PRIORITY:
        try:
            if model["provider"] == "gemini":
                print(f"Using Gemini ({model['id']})...")
                result = call_gemini(prompt, model["id"])
            elif model["provider"] == "groq":
                print(f"Using Groq ({model['id']})...")
                result = call_groq(prompt, model["id"])
            else:
                continue
 
            # ✅ Only return if we got a real non-empty response
            if result and result.strip():
                return result
 
        except Exception as e:
            print(f"{model['name']} failed: {e}")
            time.sleep(1)
            continue
 
    print("❌ All models failed. Returning None.")
    return None
 