import subprocess
from config.config import OLLAMA_MODEL_NAME

def launch_model_if_needed():
    try:
        # Vérifie si le modèle est déjà lancé
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        if OLLAMA_MODEL_NAME.split(":")[0] not in result.stdout:
            print(f"🔄 Modèle {OLLAMA_MODEL_NAME} non trouvé. Lancement en cours...")
            subprocess.run(["ollama", "pull", OLLAMA_MODEL_NAME])
        else:
            print(f"✅ Modèle {OLLAMA_MODEL_NAME} déjà disponible.")
    except Exception as e:
        print(f"❌ Erreur lors du lancement du modèle Ollama : {e}")
