# Architecture – ThinkIA

## Vue d'ensemble

Architecture multi-agent orchestrée manuellement (sans framework Crew). Chaque agent est un script Python qui utilise des providers LLM interchangeables.

## Schéma de principe

```
[Agent] → [Provider LLM] → [Ollama / Gemini / OpenRouter]
    ↓
[Tâche] → [Outils] → [Web scraping, Search, etc.]
```

## Stack technique

| Couche | Technologie |
|---|---|
| Langage | Python 3.10+ |
| Providers | Ollama, Gemini, OpenRouter |
| Web scraping | trafilatura, beautifulsoup4 |
| Recherche | ddgs (DuckDuckGo) |
| UI (futur) | Streamlit |

## Architecture des providers

```
llm_provider.py (interface)
├── ollama_provider.py    → Ollama (local)
├── gemini_provider.py    → Google Gemini API
└── openrouter_provider.py → OpenRouter API

ollama_manager.py (gestion du processus Ollama)
sablier.py (rate limiter)
```

Les providers sont sélectionnés via `config/config.py`.

## Structure des agents

Chaque agent suit un pattern :
1. Chargement du system prompt depuis `prompts/sys_msgs.py`
2. Initialisation du provider LLM
3. Exécution de la tâche (diagnostic, recherche, etc.)
4. Retour du résultat structuré

## Points d'entrée

- `iapps/diagnostic/diagnostic_ia_agents.py` – diagnostic médical
- `iapps/i-search/search_agent.py` – recherche intelligente
