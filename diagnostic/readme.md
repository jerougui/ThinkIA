# 🧠 Diagnostic Agent Médical avec IA

Ce projet est un agent conversationnel médical qui utilise un modèle de langage (`phi4-mini`) pour poser des questions pertinentes à un patient, analyser ses réponses, et produire un rapport de diagnostic complet avec recommandations.

## 🚀 Fonctionnalités

- Sablier animé avec message dynamique pour chaque étape du diagnostic
- Génération **interactive** et **adaptative** de questions médicales
- Réflexion basée sur les réponses précédentes pour éviter les doublons
- Rapport de diagnostic personnalisé
- Interface en ligne de commande (CLI) intuitive

## 📦 Prérequis

- Python ≥ 3.8
- `ollama` installé et configuré localement avec le modèle `phi4-mini`

```bash
pip install ollama
ollama pull phi4-mini
```
une fois ollama installer, lancer le modèle comme suit :
```bash
ollama run phi4-mini
```
## 🖥️ Pour les utilisateurs
Clonez le projet :

```bash
git clone https://github.com/ton_user/ThinkIA.git
cd ThinkIA
```
Installez les dépendances :

```bash
pip install -r requirements.txt
```

📂 Structure du projet
```
ton_projet/
│
├── diagnostic/
│   └── diagnostic_ia_agents.py
│   └── readme.md
│
├── tools/
│   └── sablier.py

diagnosic/diagnostic_ia_agents.py      → Script principal
tools/sablier.py                       → Animation sablier personnalisée
diagnosic/README.md                    → Documentation du projet
```
▶️ Exécution
```bash
python diagnostic/diagnostic_ia_agents.py
```
🛠️ Personnalisation
Tu peux modifier MAX_QUESTIONS pour ajuster le nombre de questions posées

Le sablier peut afficher des messages adaptés à chaque étape

Le prompt système est entièrement personnalisable pour cibler d'autres pathologies

🤖 Modèle utilisé
phi4-mini — petit modèle de langage rapide, idéal pour des scénarios médicaux légers

📜 Licence
Libre pour usage personnel ou éducationnel. L’utilisation en production médicale nécessite une validation réglementaire.


---

## 🧭 Schéma de Use Case — Agent Médical IA

Voici une représentation simplifiée des interactions principales dans ton projet :

```plaintext
[Utilisateur] ⟶ Saisit le sujet médical et ses informations personnelles
        ↓
[Agent IA] ⟶ Génère une question médicale pertinente
        ↓
[Utilisateur] ⟶ Répond à la question
        ↓
[Agent IA] ⟶ Analyse la réponse + adapte la prochaine question
        ↓
[Répéter jusqu'à MAX_QUESTIONS]
        ↓
[Agent IA] ⟶ Génère un diagnostic + recommandations
        ↓
[Utilisateur] ⟶ Consulte le rapport final
```

## Exemple :

>>\ThinkIA>python diagnostic/diagnostic_ia_agents.py
🔍 Saisis le sujet médical à explorer (ex : diabète, asthme...) : fatigue
🩺 Veuillez répondre aux questions suivantes :

Nom du patient : Bob
Âge du patient : 30
Sexe (H/F) : H
Poids (kg) : 81
Taille (cm) : 183


🧠 Question 1 : Comment décririez-vous votre niveau de fatigue récent? Est-il constant tout au long de la journée, ou varie-t-il selon les moments spécifiques ?
✏️ Votre réponse : non, généralement après le petit déjeuner ou après un repas copieux le midi


🧠 Question 2 : Vous avez mentionné que la fatigue survient après vos repas du matin et du midi. Avez-vous remarqué d'autres symptômes associés à cette période de fatigue, comme un gonflement abdominal ou une sensation de malaise ?
✏️ Votre réponse : plutot après prise d'un aliment sucré comme le café avec chocolat ou dessert copieu


🧠 Question 3 : Compte tenu du lien entre votre fatigue et la consommation de sucres raffinés, avez-vous remarqué d'autres changements qui pourraient coïncider avec ces moments de fatigue, comme des baisses soudaines d'énergie ou un état général de léthargie ? De plus, quelle est l'étendue globale de vos niveaux de fatigue durant le reste de la journée?
✏️ Votre réponse : après exercice de sport la veille, je ne pratique pas souvent la course à pied, du coup la fatigue vient apr
ès 1 ou 2 jours après


🧠 Question 4 : Pouvez-vous décrire plus précisément votre expérience de fatigue après l'exercice du sport? Y a-t-il un schéma particulier avec le type ou la durée d'activité physique que vous faites ? Avez-vous également observé une fluctuation dans les niveaux de fatigue en fonction des jours où vous n'entrez pas au tout près, comme lors d'une semaine plus calme sans entraînements intensifs ?
✏️ Votre réponse : l'exercice consiste à courir à pied avec une amplitude de 9km à l'heure, pour une distance environ 9km les dimanches matin, des fluctuation de fatigue peut se produire en cas de manque de sommeil également


🧠 Question 5 : En considérant le fait que votre routine d'exercice est relativement constante avec la course du week-end, avez-vous remarqué si l'intensité ou la durée de cette activité a changé récemment? De plus, comment visez-vous à gérer vos heures de sommeil et les changements potentiels dans votre niveau de fatigue en relation avec ces deux facteurs (exercice et sommeil) 
?
✏️ Votre réponse : c'est plutot un mélange de tous ces facteurs, sommeil, travail mental, récupération tradive et lente après exercices hebdomadaires


🩺 Diagnostic et recommandations :

Diagnostic:
Le patient Bob présente des symptômes chroniques d'épuisement post-exertional typique suite à l'exercice physique intense. Les manifestations indiquent une relation possible entre le régime alimentaire sucré (notamment les aliments riches en sucre comme le café au chocolat et la pâtisserie), un manque de sommeil, ainsi qu'une activité physique intensive sans adéquation suffisante pour la récupération.

Diagnostic principal : Fatigue post-exertionnelle
Diagnostic complémentaires :
1. Dysrégulation possible des habitudes alimentaires incluant une consommation excessive d'aliments riches en sucre.
2. Risque potentiel de troubles du sommeil ou insuffisance relative au manque de sommeil mentionné, contribuant à l'épuisement.
Recommandations :

1. Alimentation : Il est conseillé pour le patient Bob d'améliorer son régime alimentaire en évitant la consommation excessive de sucres raffinés et riches en sucre qui peuvent contribuer aux fluctuations énergétiques.
2. Suivi du mode de vie : Le maintien des niveaux modérés d'activité physique peut aider à prévenir les symptômes, mais l'importance est sur une activité régulière 
sans excès pour permettre un bon processus de récupération.
3. Gestion du sommeil : Bob devrait être encouragé à adopter des habitudes saines en matière de sommeil (par exemple, 7-9 heures par nuit) et maintenir sa cohérence afin d'améliorer la qualité globale du repos.
4. Surveillance : Il est recommandé que le patient surveille ses niveaux de fatigue tout au long de la semaine pour identifier les schémas ou déclencheurs spécifiques pouvant nécessiter des ajustements dans son style de vie.

Il pourrait être utile de suivre Bob pendant une période plus longue, en notant précisément sa nutrition et d'autres activités quotidiennes (taux d'activité physique, temps passé à travailler mentalement, etc.) pour mieux comprendre les facteurs contribuant au symptôme. Si le problème persiste ou s'aggrave, des évaluations médicales supplémentaires pourraient être nécessaires.

# Conclusion : 
NB -> choix du modèle est très important pour avoir une meilleure pertinence d'un diagnostic type médical