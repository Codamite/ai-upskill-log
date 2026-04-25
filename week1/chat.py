"""Terminal chatbot"""

import anthropic
import os
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

MODEL = 'claude-haiku-4-5-20251001'
MAX_TOKENS = 1000

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def ask(question: str, history: list) -> tuple[str | None, list]:
    """Send a single-turn question to Claude and return the response text."""

    history.append({'role': 'user', 'content': question})

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=history
        )
    except anthropic.APIError as e:
        print(f"API error: {e}")
        history.pop()
        return None, history

    response_text = message.content[0].text
    history.append({'role': 'assistant', 'content': response_text})

    return response_text, history


if __name__ == "__main__":
    history = []
    file_path = Path("chat.json")
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
        print("File loaded successfully.")

    try:
        while True:
            question = input("> ")
            if question in ('exit', 'break', 'quit'):
                break
            response, history = ask(question, history)
            print(response)
    finally:
        with open("chat.json", "w") as file:
            json.dump(history, file)
    print()
