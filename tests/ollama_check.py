# Forcer l’URL via environnement
import os
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# puis import ollama
import ollama
import logging

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

os.environ["NO_PROXY"] = "127.0.0.1"
ollama.base_url = "http://127.0.0.1:11434"

try:
    logging.debug("Tentative de connexion à Ollama...")
    response = ollama.chat(
        model="phi4-mini:latest",
        messages=[{"role": "user", "content": "Bonjour"}]
    )
    logging.info("Réponse reçue : %s", response)
except Exception as e:
    logging.error("Erreur de connexion : %s", e)
