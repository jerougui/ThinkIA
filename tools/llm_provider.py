# tools/llm_provider.py
from config.config import PROVIDER

if PROVIDER == 'gemini':
    from tools.gemini_provider import chat
elif PROVIDER == 'ollama':
    from tools.ollama_provider import chat
elif PROVIDER == 'openrouter':
    from tools.openrouter_provider import chat
else:
    raise ValueError(f"Provider '{PROVIDER}' non reconnu.")
