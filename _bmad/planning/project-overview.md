# ThinkIA – Aperçu du projet

## Objectif

Explorer et démontrer comment des agents IA peuvent collaborer en mode **Crew** (multi-agent orchestré) pour accomplir des tâches complexes de manière autonome.

## Type de projet

Backend / CLI Python – collection de scripts exécutables, pas un package installable.

## Structure

| Élément | Description |
|---|---|
| **Apps** | `iapps/diagnostic/` (diagnostic médical), `iapps/i-search/` (recherche intelligente) |
| **Providers LLM** | Ollama (local), Gemini (Google), OpenRouter (multi-modèle distant) |
| **Config** | `config/config.py` – sélection du provider, modèle, clés API |
| **Prompts** | `prompts/sys_msgs.py` – messages système pour les agents |
| **Tests** | `tests/ollama_check.py` |

## Stack technique

- **Langage :** Python 3.10+
- **Orchestration :** multi-agent manuelle (pas de framework Crew)
- **LLM locaux :** Ollama
- **LLM distants :** Google Gemini API, OpenRouter API
- **Web :** Streamlit (déclaré, non utilisé actuellement)
- **Web scraping :** trafilatura, beautifulsoup4, ddgs

## Entrées

```bash
python iapps/diagnostic/diagnostic_ia_agents.py
python iapps/i-search/search_agent.py
```
