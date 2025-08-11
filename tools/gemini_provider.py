# tools/gemini_provider.py
import os
from google import genai
from google.genai import types
from config.config import GEMINI_API_KEY, GEMINI_MODEL_NAME

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
client = genai.Client()

def chat(messages, stream=False, enable_reflexion=False):
    if stream:
        raise NotImplementedError("Le streaming n'est pas encore pris en charge pour Gemini.")

    prompt = "\n".join([msg["content"] for msg in messages if msg["role"] in ["system", "user"]])

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=None if enable_reflexion else 0
        )
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt,
        config=config
    )

    if not response or not hasattr(response, "text") or not response.text:
        raise ValueError("Réponse vide ou invalide du modèle Gemini.")

    return {
        "message": {
            "content": response.text
        }
    }
