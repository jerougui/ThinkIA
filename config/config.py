# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = 'gemini'  # 'ollama', 'openrouter', ou 'gemini'
USE_KEYWORD_EXTRACTION = False

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL_NAME = 'gemini-2.5-flash'
GEMINI_ENABLE_REFLEXION = False

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_MODEL_NAME = 'mistralai/mistral-small-3.2-24b-instruct:free'
OLLAMA_MODEL_NAME = 'phi4-mini:latest'
# cognitivecomputations/dolphin-mistral-24b-venice-edition:free
# deepseek/deepseek-chat-v3-0324:free
# 'mistralai/mistral-small-3.2-24b-instruct:free'
# qwen/qwen3-coder:free

OPENROUTER_HEADERS = {
    "HTTP-Referer": "https://jam-ai.fr",
    "X-Title": "JamAI Assistant"
}
