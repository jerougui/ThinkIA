import streamlit as st
import os

from tools.openrouter_provider import chat as openrouter_chat
from tools.ollama_provider import chat as ollama_chat

SYSTEM_PROMPT = """Tu es un assistant de diagnostic médical expert, comme un médecin qui mène une consultation.

Règles de conversation :
- Pose UNE SEULE question à la fois, comme dans un vrai échange médical
- Attends la réponse avant de poser la question suivante
- Sois naturel et empathique, pas robotique
- Utilise les réponses précédentes pour adapter ta question suivante
- Quand tu as assez d'informations, fournis une analyse structurée avec :
  1. Symptômes identifiés
  2. Causes possibles (par ordre de probabilité)
  3. Recommandations et précautions
  4. Signes d'alerte nécessitant une consultation urgente

Réponds en français, de manière claire et professionnelle."""


def check_ollama():
    try:
        from ollama import Client
        client = Client()
        client.list()
        return True
    except Exception:
        return False


def get_api_key_status():
    openrouter_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")
    return bool(openrouter_key)


def render_chat():
    st.title("🧠 ThinkIA — Diagnostic Médical")
    st.markdown("Posez vos symptômes, l'assistant vous aide à y voir plus clair.")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "provider" not in st.session_state:
        st.session_state.provider = "OpenRouter"
    if "ollama_available" not in st.session_state:
        st.session_state.ollama_available = check_ollama()

    with st.sidebar:
        st.header("Configuration")

        provider_options = ["OpenRouter"]
        if st.session_state.ollama_available:
            provider_options.append("Ollama")

        selected_provider = st.selectbox(
            "Provider LLM",
            provider_options,
            index=provider_options.index(st.session_state.provider)
            if st.session_state.provider in provider_options
            else 0,
        )
        st.session_state.provider = selected_provider

        if not st.session_state.ollama_available:
            st.info("Ollama non détecté. Utilisez OpenRouter.")
        if not get_api_key_status():
            st.warning("Clé API OpenRouter non configurée.")

        if st.button("🗑️ Nouvelle conversation"):
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Décrivez vos symptômes..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyse en cours..."):
                try:
                    if st.session_state.provider == "OpenRouter" and not get_api_key_status():
                        raise ValueError(
                            "OPENROUTER_API_KEY non configurée. Configurez-la dans "
                            "`.streamlit/secrets.toml` (local) ou les secrets Streamlit Cloud."
                        )

                    if st.session_state.provider == "Ollama" and not st.session_state.ollama_available:
                        raise ConnectionError(
                            "Ollama n'est pas disponible localement. "
                            "Vérifiez qu'Ollama est lancé (http://localhost:11434)."
                        )

                    chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for msg in st.session_state.messages:
                        chat_messages.append(
                            {"role": msg["role"], "content": msg["content"]}
                        )

                    if st.session_state.provider == "OpenRouter":
                        response = openrouter_chat(chat_messages)
                    else:
                        response = ollama_chat(chat_messages)

                    content = response["message"]["content"]
                    st.markdown(content)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": content}
                    )

                except ValueError as e:
                    st.error(str(e))
                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"⚠️ {e}"}
                    )
                except ConnectionError as e:
                    st.error(str(e))
                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"⚠️ {e}"}
                    )
                except Exception as e:
                    error_msg = f"Désolé, une erreur est survenue : {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
