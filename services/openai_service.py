import os
import json
from services.session_memory import (
    get_conversation,
    save_conversation
)
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-4o-mini"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def chat_completion(system_prompt, user_input, session_id):

    try:

        conversation = get_conversation(session_id)

        if conversation is None:
            conversation = []

        conversation.append({
            "role": "user",
            "content": user_input
        })

        save_conversation(session_id, conversation)

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(conversation)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        ai_message = response.choices[0].message.content

        conversation.append({
            "role": "assistant",
            "content": str(ai_message)
        })

        save_conversation(session_id, conversation)

        try:
            return json.loads(ai_message)

        except:
            return str(ai_message)

    except Exception as e:

        print("OPENAI ERROR:", e)

        return {
            "error": str(e)
        }