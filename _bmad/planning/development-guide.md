# Guide de développement – ThinkIA

## Prérequis

- Python 3.10+
- Ollama (pour les modèles locaux)
- Comptes API : Gemini, OpenRouter (optionnel)

## Installation

```bash
git clone https://github.com/jerougui/ThinkIA.git
cd ThinkIA
pip install -r requirements.txt
```

## Configuration

Créer un fichier `.env` à la racine :

```text
GEMINI_API_KEY=<votre_clé>
OPENROUTER_API_KEY=<votre_clé>
```

Configurer le provider et le modèle dans `config/config.py`.

## Exécution

```bash
# Diagnostic médical
python iapps/diagnostic/diagnostic_ia_agents.py

# Recherche intelligente
python iapps/i-search/search_agent.py
```

## Tests

```bash
python tests/ollama_check.py
```
