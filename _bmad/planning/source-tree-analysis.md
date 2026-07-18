# Analyse de l'arborescence source

```
ThinkIA/
├── _bmad/                          # Méthode BMad (documentation, config)
│   ├── bmm/config.yaml
│   ├── planning/                   # Documentation générée
│   └── stories/
├── config/
│   └── config.py                   # Configuration centrale : provider, modèle, clés
├── iapps/                          # Applications multi-agent
│   ├── diagnostic/
│   │   ├── diagnostic_ia_agents.py # Agent de diagnostic médical
│   │   └── readme.md
│   └── i-search/
│       ├── README.md
│       └── search_agent.py         # Agent de recherche intelligente
├── prompts/
│   └── sys_msgs.py                 # Messages système des agents
├── resources/
│   └── img/                        # Images (captures, schémas)
├── tests/
│   └── ollama_check.py             # Vérification de la connectivité Ollama
├── tools/                          # Couche d'accès aux LLM
│   ├── gemini_provider.py
│   ├── llm_provider.py            # Interface commune
│   ├── ollama_manager.py
│   ├── ollama_provider.py
│   ├── openrouter_provider.py
│   └── sablier.py                  # Rate limiter
├── .env                            # Clés API (non versionné)
├── .gitignore
├── README.md
├── readme-bmad.md
└── requirements.txt
```

## Dossiers critiques

| Dossier | Rôle |
|---|---|
| `tools/` | Abstraction des fournisseurs LLM (interface commune + implémentations) |
| `iapps/` | Applications concrètes utilisant les agents en mode Crew |
| `prompts/` | Prompts système partagés entre les agents |
| `config/` | Point de configuration central |
