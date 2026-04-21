"""Ask Claude a question from command line"""

import anthropic
import os
import sys
from dotenv import load_dotenv

load_dotenv()

MODEL = 'claude-haiku-4-5-20251001'
MAX_TOKENS = 1000

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def ask(question: str) -> str:
    """Send a single-turn question to Claude and return the response text."""
    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
    except anthropic.APIError as e:
        print(f"API error: {e}")
        return None

    return message.content[0].text


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Explain embeddings in one paragraph."
    print(ask(question))
    print()
