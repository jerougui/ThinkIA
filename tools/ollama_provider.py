from ollama import Client
from config.config import OLLAMA_MODEL_NAME

client = Client()

def chat(messages, stream=False):
    formatted_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in messages
        if msg["role"] in ["system", "user"]
    ]

    response = client.chat(
        model=OLLAMA_MODEL_NAME,
        messages=formatted_messages,
        stream=stream
    )

    if stream:
        return response
    else:
        return {
            "message": {
                "content": response["message"]["content"]
            }
        }
