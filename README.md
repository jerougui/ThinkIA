# THINKIA – Exemples d'Agents IA en mode Crew

Ce projet présente des exemples concrets d'utilisation des techniques d'agents IA organisés en mode **Crew**, c’est-à-dire des agents collaborant pour accomplir des tâches complexes de manière autonome et coordonnée.

## 📁 Structure du projet
```
THINKIA/
├── config/
├── iapps/
│   └── diagnostic/
│       ├── diagnostic_ia_agents.py
│       └── readme.md
├── i-search/
│   ├── README.md
│   └── search_agent.py
├── prompts/
│   └── sys_msgs.py
├── resources/
│   └── img/
│       ├── console_example01.png
│       └── schema_diagram.png
├── tests/
│   └── ollama_check.py
├── tools/
│   ├── gemini_provider.py
│   ├── llm_provider.py
│   ├── ollama_manager.py
│   ├── ollama_provider.py
│   ├── openrouter_provider.py
│   └── sablier.py
├── .env
└── .gitignore

```
# Avant de commencer

## Prérequis :
 [Python 3.10+](https://www.python.org/downloads/)
 ## 📖 Documentation Ollama

Pour démarrer rapidement avec Ollama et exécuter des modèles localement, consulte la section [Quickstart de la documentation officielle](https://github.com/ollama/ollama/blob/main/README.md#quickstart) sur GitHub.

## 🚀 Documentation OpenRouter

Pour intégrer rapidement OpenRouter et accéder à des centaines de modèles via une API unifiée, consulte le [guide Quickstart officiel](https://openrouter.ai/docs/quickstart).

 ## QuickStart
```bash
# Cloner le dépôt
git clone https://github.com/jerougui/ThinkIA.git
cd ThinkIA

```
🔐 Configuration des clés API
Pour que l’agent fonctionne correctement, tu dois créer un fichier .env à la racine du projet. Ce fichier contient les clés API privées nécessaires à la communication avec les modèles d’IA.

📄 Exemple de fichier `.env :
```text
# 🔐 Clés API
GEMINI_API_KEY=<GEMINI_API_KEY>
OPENROUTER_API_KEY=<OPENROUTER_API_KEY>
````

## Installer les dépendances
```bash
pip install -r requirements.txt

python -m pip install -r requirements.txt
```
---

## 🚀 Lancer les exemples

### 🩺 Diagnostic médical assisté par agents IA
```bash
python iapps/diagnostic/diagnostic_ia_agents.py
```
➡️ Voir [iapps/diagnostic/readme.md](iapps/diagnostic/readme.md) pour plus d'informations.

## 🔍 Recherche intelligente par agents IA
```bash
python iapps/i-search/search_agent.py
```
➡️ Voir [iapps/i-search/readme.md](iapps/i-search/readme.md) pour plus d'informations.

## 🎯 Objectif du projet
Démontrer comment des agents IA peuvent être orchestrés en mode Crew pour :

Simuler des environnements intelligents

Réaliser des tâches complexes en autonomie

Collaborer via des rôles spécialisés

## 🛠️ Technologies utilisées
Python

Modèles LLM via ollama, openrouter, etc.

Architecture multi-agent Crew

Prompts dynamiques et contextuels

## 📚 Ressources
Chaque exemple contient son propre readme.md avec des détails sur :

Le rôle des agents

Le workflow collaboratif

Les cas d’usage simulés

## 🛠️ Technologies utilisées

- Agents IA orchestrés en mode Crew
- Intégration avec des LLM en local à l'aide de `ollama` ou  via des providers (`gemini`, `openrouter`, etc.)
- Prompts dynamiques et messages système personnalisés
- Scripts Python modulaires et testables

## 🤖 Utilisation des modèles LLM

Les agents IA de ce projet s'appuient sur des **modèles de langage (LLM)** accessibles via deux modes :

### 🔐 Mode local (exécution privée garantie)
Les modèles sont exécutés **en local** via des outils comme `Ollama`, garantissant :
- Aucune donnée envoyée à des serveurs externes
- Contrôle total sur les interactions et les logs
- Confidentialité maximale pour les scénarios sensibles

### 🌐 Mode provider (accès à des modèles distants)
Les agents peuvent également interagir avec des **providers externes** comme `OpenRouter`, permettant :
- Accès à des modèles avancés hébergés à distance
- Flexibilité dans le choix des capacités et des coûts
- Adaptabilité selon les besoins du projet

> Le mode d'exécution (local ou provider) peut être configuré dynamiquement selon le contexte ou les préférences de l'utilisateur.

## 🎯 Objectif

Explorer et démontrer comment des agents IA peuvent collaborer efficacement dans des contextes variés, en simulant des environnements réels et des workflows intelligents.

---

