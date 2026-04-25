import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

MODEL = 'claude-haiku-4-5-20251001'
MAX_TOKENS = 500

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

PERSONAS = {
    "strict_reviewer": "You are a strict reviewer who is skeptical and points out what's wrong with common approaches",
    "enthusiastic_teacher": "You are an enthusiastic teacher who uses lots of metaphors and encouragement",
    "terse_expert": "You are a terse expert who only responds in bullet points, no more than 5 bullets"
}


def ask(question: str, system_prompt: str | None = None) -> str:
    kwargs = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }

    if system_prompt:
        kwargs["system"] = system_prompt

    message = client.messages.create(**kwargs)
    response_text = message.content[0].text
    print(response_text)
    print()
    return response_text


for name, system_prompt in PERSONAS.items():
    print(f"================={name}====================")
    ask(question='how do I learn data engineering?', system_prompt=system_prompt)
    print()

print("=== strict_reviewer (in user message) ===")
ask(question='You are a strict reviewer who points out every flaw.how should I learn data engineering?',
    system_prompt=None)


