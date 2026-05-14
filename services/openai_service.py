import os
import json

from services.session_memory import conversation_memory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-4o-mini"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def chat_completion(system_prompt, user_input, session_id):

    try:

        if session_id not in conversation_memory:
            conversation_memory[session_id] = []

        conversation_memory[session_id].append({
            "role": "user",
            "content": user_input
        })

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(conversation_memory[session_id])

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        ai_message = response.choices[0].message.content

        conversation_memory[session_id].append({
            "role": "assistant",
            "content": str(ai_message)
        })

        return str(ai_message)

    except Exception as e:

        print("OPENAI ERROR:", e)

        return {
            "error": str(e)
        }