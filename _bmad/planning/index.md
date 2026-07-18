# ThinkIA – Index de la documentation

## Aperçu

- **Type :** Monolith
- **Langage :** Python 3.10+
- **Architecture :** Multi-agent Crew avec providers LLM interchangeables

## Documentation générée

- [Aperçu du projet](./project-overview.md)
- [Architecture](./architecture.md)
- [Analyse de l'arborescence](./source-tree-analysis.md)
- [Guide de développement](./development-guide.md)

## Documentation existante

- [README principal](../../README.md) – Présentation générale, setup, usage
- [readme-bmad](../../readme-bmad.md) – Workflow BMad
- [Diagnostic - readme](../../iapps/diagnostic/readme.md)
- [i-Search - README](../../iapps/i-search/README.md)

## Pour commencer

```bash
pip install -r requirements.txt
python iapps/diagnostic/diagnostic_ia_agents.py
```

## Prochaines étapes BMad

1. Définir les objectifs avec `bmad-prd`
2. Créer l'architecture spine avec `bmad-architecture`
3. Découper en stories avec `bmad-create-epics-and-stories`
4. Planifier le sprint avec `bmad-sprint-planning`
