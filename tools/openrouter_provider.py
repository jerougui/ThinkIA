# tools/openrouter_provider.py
from openai import OpenAI
from config.config import OPENROUTER_API_KEY, OPENROUTER_MODEL_NAME, OPENROUTER_HEADERS

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def chat(messages, stream=False):
    formatted_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in messages
        if msg["role"] in ["system", "user"]
    ]

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL_NAME,
        messages=formatted_messages,
        extra_headers=OPENROUTER_HEADERS,
        stream=stream
    )

    if stream:
        return response  # Le streaming est géré dans search_agent.py
    else:
        return {
            "message": {
                "content": response.choices[0].message.content
            }
        }
