---
title: 'Chat app Streamlit pour diagnostic médical'
type: 'feature'
created: '2026-07-18'
status: 'done'
baseline_commit: '10db894bf94b0d5c8b05349f234268c0cb917539'
review_loop_iteration: 0
context:
  - '_bmad/planning/architecture/architecture-ThinkIA-2026-07-18/ARCHITECTURE-SPINE.md'
  - '_bmad/planning/prds/prd-ThinkIA-2026-07-18/prd.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** L'agent de diagnostic médical ThinkIA (`diagnostic_ia_agents.py`) est exclusivement CLI (bloquant sur `input()`/`print()`). Impossible de le tester sans installation locale, ce qui bloque la démo et la validation externe.

**Approach:** Créer une interface de chat web Streamlit monopage (`streamlit_app.py` + `chat_app.py`) qui enveloppe le pipeline LLM dans un chat browser. Les fonctions `diagnostic_ia_agents.py` ne sont pas modifiées — `chat_app.py` utilise directement `tools.llm_provider.chat()` avec ses propres prompts.

## Boundaries & Constraints

**Always:**
- AD-1 à AD-5 (Architecture Spine) — Streamlit monopage, session state, secrets, point d'entrée unique
- `diagnostic_ia_agents.py`, `config/config.py` et les providers ne sont PAS modifiés
- `st.chat_input` + `st.chat_message` pour l'UI — pas de framework additionnel
- Sélecteur de provider dans la sidebar (Ollama en local, OpenRouter en cloud)

**Ask First:**
- Ajout d'un provider Gemini dans le sélecteur ? (actuellement non prévu dans l'architecture, mais détectable via `PROVIDER`)

**Never:**
- Pas d'authentification, pas de base de données, pas de persistance entre sessions
- Pas de modification des fichiers existants (`diagnostic_ia_agents.py`, providers, `config.py`)
- Pas de JS ou framework web externe

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| HAPPY_PATH | Symptôme tapé dans le chat | Réponse diagnostique structurée de l'agent | N/A |
| MISSING_API_KEY | OPENROUTER_API_KEY absente et provider OpenRouter sélectionné | Message : "Service temporairement indisponible. Vérifiez la configuration de la clé API." | Désactiver l'envoi, afficher l'erreur dans le chat |
| OLLAMA_UNAVAILABLE | Ollama sélectionné mais serveur injoignable | Message : "Ollama n'est pas disponible localement." | Basculer la sélection sur OpenRouter si clé présente |
| EMPTY_MESSAGE | Champ vide + bouton Envoyer | Rien ne se passe | Ignorer silencieusement |
| SESSION_RESET | Clic sur "Nouvelle conversation" | `st.session_state` réinitialisé, chat vidé | N/A |

</frozen-after-approval>

## Code Map

- `streamlit_app.py` -- Point d'entrée Streamlit Cloud (racine)
- `iapps/diagnostic/chat_app.py` -- Logique de chat UI + intégration LLM
- `.streamlit/secrets.toml` -- Secrets locaux (gitignoré)
- `.gitignore` -- Ajout de `.streamlit/`

## Tasks & Acceptance

**Execution:**
- [x] `.gitignore` -- Ajouter `.streamlit/` à la liste des ignorés
- [x] `.streamlit/secrets.toml` -- Créer le fichier template de secrets locaux (modèle vide, clés à remplir par l'utilisateur)
- [x] `iapps/diagnostic/chat_app.py` -- Fonction `render_chat()` : UI de chat avec `st.chat_input`, `st.chat_message`, sélecteur de provider en sidebar, historique en session state, appel à `tools.llm_provider.chat()` avec système de prompts médical
- [x] `streamlit_app.py` -- Page Streamlit qui importe et appelle `chat_app.render_chat()` avec config de page (titre, layout)

**Acceptance Criteria:**
- Given `streamlit run streamlit_app.py` exécuté, when la page charge, alors une interface de chat s'affiche avec un titre et une zone de saisie
- Given l'utilisateur tape un symptôme et valide, when le message est envoyé, alors la réponse de l'agent apparaît dans le fil de discussion
- Given une session active, when l'utilisateur envoie plusieurs messages, alors l'historique complet est visible dans `st.session_state`
- Given le sélecteur de provider en sidebar, when l'utilisateur change de provider, alors le prochain appel LLM utilise le provider sélectionné
- Given `.gitignore` modifié, when `git status` est exécuté, alors `.streamlit/` n'apparaît pas dans les untracked files

## Verification

**Commands:**
- `streamlit run streamlit_app.py` -- expected: l'app charge sans erreur et affiche l'interface de chat
- `git status` -- expected: `.streamlit/` n'apparaît pas dans les untracked files

**Manual checks (if no CLI):**
- Ouvrir l'app dans le navigateur, envoyer un message, vérifier que la réponse arrive
- Tester "Nouvelle conversation" : le chat se vide
- Basculer entre Ollama et OpenRouter dans la sidebar
