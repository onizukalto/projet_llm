import os
import json
import requests
import streamlit as st

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODELE = "qwen2.5-coder:7b"

st.title("Mon assistant Data / ML")

# 1. La mémoire, créée une seule fois, avec la consigne cachée
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": "Tu es un expert en data science et machine learning. "
                   "Tu réponds en français, de façon claire et pédagogique, "
                   "avec des exemples de code Python quand c'est utile. "
                   "Si tu n'es pas sûr d'une réponse, dis-le.",
    }]

# 2. Réafficher l'historique, sans la consigne cachée
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 3. Nouveau message de l'utilisateur
question = st.chat_input("Pose ta question...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # 4. Recevoir la réponse morceau par morceau
    def generer():
        with requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODELE, "messages": st.session_state.messages, "stream": True},
            stream=True,
        ) as r:
            for ligne in r.iter_lines():
                if ligne:
                    morceau = json.loads(ligne)
                    yield morceau["message"]["content"]

    with st.chat_message("assistant"):
        texte = st.write_stream(generer())

    st.session_state.messages.append({"role": "assistant", "content": texte})