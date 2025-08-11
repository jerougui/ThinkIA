import sys
import os

# 📁 Accès aux modules du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.sablier import Sablier
from tools.ollama_manager import launch_model_if_needed
from config.config import PROVIDER
from tools.llm_provider import chat

MAX_QUESTIONS = 5

def collect_static_patient_info():
    print("🩺 Veuillez répondre aux questions suivantes :\n")
    nom = input("Nom du patient : ").strip()
    age = input("Âge du patient : ").strip()
    sexe = input("Sexe (H/F) : ").strip()
    poids = input("Poids (kg) : ").strip()
    taille = input("Taille (cm) : ").strip()
    return f"nommé(e) {nom}, âgé(e) de {age} ans, de sexe {sexe}, pesant {poids} kg pour {taille} cm."

def generate_context_and_questions(topic, profil_patient):
    conversation = [{
        "role": "system",
        "content": (
            f"Tu es un médecin généraliste empathique et expérimenté. "
            f"Tu interroges un patient {profil_patient} sur le sujet '{topic}' pour établir un diagnostic. "
            f"À chaque question, tu t'appuies sur les réponses précédentes pour affiner la suivante sans jamais te répéter."
        )
    }]

    resultats = []
    for i in range(MAX_QUESTIONS):
        if i == 0:
            prompt_utilisateur = (
                f"Commence par poser une première question pertinente et claire sur '{topic}'. "
                "Ne pose qu’une seule question à la fois."
            )
        else:
            historique = "\n".join(
                [f"{j+1}. Q: {r['question']}\n   R: {r['reponse']}" for j, r in enumerate(resultats)]
            )
            prompt_utilisateur = (
                f"Voici l’historique des échanges avec le patient :\n{historique}\n\n"
                f"Pose maintenant une nouvelle question utile sur '{topic}', en évitant les doublons, "
                f"et en tenant compte des réponses précédentes. Ne propose qu’une seule question."
            )

        conversation.append({"role": "user", "content": prompt_utilisateur})
        sablier = Sablier(message=f"🤖 Réflexion sur la question {i+1}/{MAX_QUESTIONS}...")
        sablier.start()
        response = chat(messages=conversation)  # ✅ modèle choisi automatiquement
        sablier.stop()

        question = response["message"]["content"]
        print(f"\n🧠 Question {i+1} : {question}")
        reponse_patient = input("✏️ Votre réponse : ").strip()

        resultats.append({
            "question": question,
            "reponse": reponse_patient
        })

        conversation.append({"role": "assistant", "content": question})
        conversation.append({"role": "user", "content": reponse_patient})

    return resultats

def create_diagnostic_and_recommandations(resultats, profil_patient, topic):
    rapport_intro = f"Le patient {profil_patient} a répondu aux questions suivantes sur le sujet '{topic}' :\n"
    for i, item in enumerate(resultats, 1):
        rapport_intro += f"{i}. Q: {item['question']}\n   R: {item['reponse']}\n"

    messages = [
        {
            "role": "system",
            "content": (
                "Tu es un médecin spécialiste qualifié. Analyse attentivement les réponses du patient "
                "et rédige un diagnostic clair, détaillé et professionnel, accompagné de recommandations concrètes."
            )
        },
        {"role": "user", "content": rapport_intro}
    ]

    sablier = Sablier(message="📋 Génération du rapport et du diagnostic en cours...")
    sablier.start()
    rapport = chat(messages=messages)  # ✅ modèle choisi automatiquement
    sablier.stop()

    print("\n🩺 Diagnostic et recommandations :\n")
    print(rapport["message"]["content"])

if __name__ == "__main__":
    if PROVIDER == 'ollama':
        launch_model_if_needed()

    topic = input("🔍 Saisis le sujet médical à explorer (ex : diabète, asthme...) : ").strip()
    profil = collect_static_patient_info()
    resultats = generate_context_and_questions(topic, profil)
    create_diagnostic_and_recommandations(resultats, profil, topic)
