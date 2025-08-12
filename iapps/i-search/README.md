# 🧠 Search Agent – Assistant IA avec Recherche Web Intelligente

**Search Agent** est un assistant intelligent en Python capable d’améliorer ses réponses grâce à des recherches web en temps réel. Il utilise des modèles IA comme ollama en local via Ollama, ou des providers distants tels que OpenRouter ou Gemini. L’agent extrait des mots-clés sémantiques, interroge DuckDuckGo ou Google, sélectionne les résultats les plus pertinents et génère des réponses contextualisées.

---

![Schéma et processus ](/resources/img/schema_diagram.png)

## 🚀 Fonctionnalités

- ✅ Extraction sémantique des mots-clés à partir de l’entrée utilisateur
- 🔍 Recherche web via DuckDuckGo ou Google
- 🧭 Sélection intelligente du meilleur résultat
- 📄 Scraping de pages web + filtrage contextuel
- 🤖 Réponses enrichies en utilisant différents modèles llm en local ou distant
- 🎨 Affichage coloré dans le terminal grâce à Colorama

---

## 📦 Installation

Prérequis : [Python 3.10+](https://www.python.org/downloads/)

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
# Exemple 
## Pré-requis : ollama
Assure-toi que Ollama est bien installé et que le modèle phi4-mini est lancé :

```bash
ollama serve # s'il n'est pas encore lancer

ollama run phi4-mini:latest

# vérifi que le modèle est bien lancé
ollama ps
```
remarque le script tentera de lancer ollama en local si ce dernier n'est pas lancé.

## ▶️ lancement du programme 
Exécute le script depuis la racine du projet :

```bash
ThinkIA> python iapps/i-search/search_agent.py
```

Exemple d’entrée utilisateur :
```bash
 cherche deux informations interessante (innovation et ou insolite) qui s'est produite aujourd'hui 04/08/2025
```

## 🖥️ Exemple de sortie console
![Exemple de sortie console](/resources/img/console_example01.png)

# Reférence : 
https://www.youtube.com/watch?v=9KKnNh89AGU