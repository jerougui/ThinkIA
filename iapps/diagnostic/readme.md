# 🩺 Assistant Diagnostic Médical Interactif
Ce projet est un assistant médical interactif conçu pour simuler une consultation entre un médecin généraliste et un patient. Il utilise un modèle de langage pour poser des questions pertinentes, analyser les réponses, et générer un diagnostic accompagné de recommandations.

## 🚀 Fonctionnalités
Collecte des informations statiques du patient (nom, âge, sexe, poids, taille)

Génération dynamique de 5 questions médicales personnalisées selon un sujet donné

Interaction en temps réel avec le patient via la console

Synthèse des réponses et création d’un rapport médical détaillé

Intégration avec différents fournisseurs LLM (ex : Ollama)

## 📦 Structure du projet
```
project/
│
├── main.py                      # Script principal
├── config/
│   └── config.py                # Configuration du fournisseur LLM
├── tools/
│   ├── sablier.py              # Animation console pour attente
│   ├── ollama_manager.py       # Lancement du modèle Ollama si nécessaire
│   └── llm_provider.py         # Interface avec le modèle de langage
```
## 🧠 Technologies utilisées
Python 3.10+

## Modèle de langage (LLM) via chat() abstrait

Console interactive

Intégration avec Ollama (optionnel)

## 📝 Utilisation
Clone le dépôt :

```bash
git clone https://github.com/jerougui/ThinkIA.git
```
Installe les dépendances nécessaires :

```bash
pip install -r requirements.txt
```
Lance le script :

```bash
ThinkIA>python iapps/diagnostic/diagnostic_ia_agents.py
```
Suis les instructions dans la console :

Saisis le sujet médical (ex : diabète)

Réponds aux questions posées

Consulte le diagnostic généré

## ⚙️ Configuration
Le fichier config/config.py permet de définir le fournisseur de modèle :

```python
PROVIDER = 'ollama'  # ou 'openai', 'local', etc.
📌 Exemple d’utilisation
text
🔍 Saisis le sujet médical à explorer (ex : diabète, asthme...) : asthme
🩺 Veuillez répondre aux questions suivantes :
Nom du patient : Alice
Âge du patient : 34
Sexe (H/F) : F
Poids (kg) : 62
Taille (cm) : 168

🧠 Question 1 : Depuis combien de temps ressentez-vous des difficultés respiratoires ?
✏️ Votre réponse : Depuis environ 2 ans.
...
```
## 🩺 Diagnostic et recommandations :
Le tableau clinique suggère un asthme modéré. Il est recommandé de...
## 📄 Licence
Ce projet est sous licence MIT. (utiliser, modifier et distribuer librement).