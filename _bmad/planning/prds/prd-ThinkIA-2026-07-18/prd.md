---
title: ThinkIA – Diagnostic Chat Web
created: 2026-07-18
updated: 2026-07-18
status: final
---

# PRD: ThinkIA – Diagnostic Chat Web

## 0. Objectif du document

Ce PRD décrit l'ajout d'une interface web de chat interactive pour le module de diagnostic médical (`iapps/diagnostic/diagnostic_ia_agents.py`) de ThinkIA, ainsi que le déploiement sur Streamlit Community Cloud avec gestion sécurisée des clés API. Il s'adresse au développeur du projet (jerougui) et contient les stories à implémenter.

## 1. Vision

Permettre à un visiteur d'interagir avec l'agent de diagnostic médical ThinkIA depuis un navigateur, via une console de chat simple et intuitive, sans installation locale. Le code reste open source sur GitHub, les clés API sont injectées de manière sécurisée.

## 2. Utilisateur cible

### 2.1 Jobs To Be Done

- Découvrir et tester le diagnostic médical multi-agent sans installation
- Présenter le projet à un recruteur, un collègue ou lors d'une démo
- Explorer le comportement des agents IA en mode Crew

### 2.2 Non-Users (v1)

- Pas de gestion de comptes utilisateurs
- Pas de persistance des sessions
- Pas de mobile natif (responsive Streamlit suffit)

### 2.3 Key User Journeys

**UJ-1. Un visiteur teste le diagnostic médical.**
- **Persona + contexte :** Un développeur curieux tombe sur le repo GitHub, clique le badge Streamlit.
- **Entrée :** Page d'accueil du chat Streamlit.
- **Chemin :**
  1. Lit une courte description du projet
  2. Tape un symptôme dans la zone de chat (ex: "J'ai mal à la tête et de la fièvre")
  3. L'agent diagnostiqueur répond avec une analyse structurée
  4. Continue la conversation pour préciser le diagnostic
- **Climax :** Reçoit un diagnostic cohérent qui montre la valeur du multi-agent.
- **Résolution :** Satisfait, il peut cloner le repo ou explorer le code source.
- **Edge case :** Si OPENROUTER_KEY n'est pas configurée → message clair : "Service temporairement indisponible."

## 3. Glossaire

- **Chat web** — Interface de discussion en temps réel dans le navigateur, utilisant Streamlit
- **Agent diagnostic** — Script Python `diagnostic_ia_agents.py` qui orchestre les agents Crew
- **Streamlit Community Cloud** — Plateforme d'hébergement gratuite liée à GitHub, avec support des secrets
- **OPENROUTER_API_KEY** — Clé d'API pour le fournisseur OpenRouter, stockée comme secret GitHub/Streamlit

## 4. Features

### 4.1 Interface de chat Streamlit

**Description :** Créer une app Streamlit (`iapps/diagnostic/chat_app.py`) qui :
- Affiche une zone de chat type messaging
- Capture les entrées utilisateur et les envoie à l'agent diagnostic
- Affiche les réponses de l'agent en temps réel
- Gère l'historique de la conversation dans la session

**Functional Requirements:**

#### FR-1: Envoi et réception de messages

L'utilisateur peut envoyer un message texte via un champ de saisie. Le message est transmis à l'agent diagnostic. La réponse est affichée dans la zone de chat.

**Conséquences (testables) :**
- Le message utilisateur apparaît immédiatement dans le chat (côté utilisateur)
- La réponse de l'agent apparaît dans un délai < 30s (timeout configurable)

#### FR-2: Gestion de session

L'historique des messages est conservé pendant la session Streamlit. Un bouton "Nouvelle conversation" réinitialise le contexte.

#### FR-3: Sélection du provider

L'utilisateur peut choisir entre Ollama (local) et OpenRouter (distant) via un sélecteur dans la sidebar. [ASSUMPTION : le déploiement cloud utilisera OpenRouter]

### 4.2 Déploiement Streamlit Cloud

**Description :** Configuration du projet pour le déploiement automatisé sur Streamlit Community Cloud.

**Functional Requirements:**

#### FR-4: Fichier de configuration Streamlit

Créer `streamlit_app.py` à la racine pointant vers le chat, et `requirements.txt` complet incluant `streamlit`.

#### FR-5: Variables d'environnement sécurisées

`OPENROUTER_API_KEY` et `GEMINI_API_KEY` injectées via les secrets Streamlit Cloud (pas dans le repo).

**Conséquences (testables) :**
- Le repo ne contient aucune clé API en clair
- `git grep` API_KEY ne retourne que le `.env.example` et `config.py`

### 4.3 Documentation du déploiement

**Description :** Mise à jour du README et création d'un guide de déploiement.

**Functional Requirements:**

#### FR-6: Badge Streamlit et instructions

Ajouter un badge "Open in Streamlit" dans le README. Documenter les étapes pour configurer les secrets sur Streamlit Cloud.

## 5. Non-Goals (Explicites)

- Pas d'authentification utilisateur
- Pas de base de données
- Pas de déploiement autre que Streamlit Cloud (v1)
- Pas de modification du moteur de diagnostic existant

## 6. MVP Scope

### 6.1 In Scope

- Chat app Streamlit pour le diagnostic médical
- Déploiement sur Streamlit Community Cloud
- Secret OPENROUTER_API_KEY configuré
- README mis à jour avec badge et instructions

### 6.2 Out of Scope for MVP

- Support de l'agent de recherche (`i-search`) — v2
- Tests automatisés de l'UI — v2
- Monitoring / logs — v2

## 7. Success Metrics

**Primaire**
- **SM-1 :** L'app est accessible publiquement sur Streamlit Cloud dans les 24h suivant la finalisation du PRD

**Secondaire**
- **SM-2 :** Un développeur tiers peut lancer le chat sans instructions supplémentaires (README suffit)

## 8. Open Questions

1. Faut-il un fallback vers un modèle gratuit (Gemini) si OpenRouter rate un appel ?
2. Combien de temps conserver l'historique de chat ? Limité à la session uniquement ?

## 9. Stories

**Story-1 : Chat app Streamlit**
> En tant que visiteur, je peux accéder à une interface de chat web pour interagir avec l'agent diagnostic.
> **Acceptance :**
> - `streamlit_app.py` existe à la racine
> - La zone de chat s'affiche et accepte la saisie
> - L'agent répond via OpenRouter (ou Ollama en local)
> - L'historique est conservé pendant la session

**Story-2 : Déploiement Streamlit Cloud**
> En tant que mainteneur, je peux déployer l'app sur Streamlit Cloud avec les clés API sécurisées.
> **Acceptance :**
> - Le repo est poussé sur GitHub
> - Streamlit Cloud est connecté au repo
> - OPENROUTER_API_KEY est configurée dans les secrets Streamlit
> - L'app est accessible publiquement

**Story-3 : Badge README et documentation**
> En tant que visiteur GitHub, je vois un badge "Open in Streamlit" et des instructions de déploiement dans le README.
> **Acceptance :**
> - Badge Streamlit présent en haut du README
> - Section "Déploiement" documentée avec les étapes
