from dotenv import load_dotenv
from core.models import Verb
import anthropic
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_examples(verb: Verb) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Give me 3 example sentences with the verb '{verb.english}' (meaning: {verb.russian}), using V1, V2, and V3 forms. For each sentence add a Russian translation."}
        ]
    )
    return message.content[0].text # type: ignore

def get_translation_task(verb: Verb) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Give me a sentence with the verb '{verb.english}' (meaning: {verb.russian}) in Russian and ask to translate it to English using the correct form of the verb (V1, V2, or V3)."}
        ]
    )
    return message.content[0].text # type: ignore

def check_translation(verb: Verb, task: str, user_translation: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Task: {task}\nVerb: '{verb.english}' ({verb.russian})\nUser translation: '{user_translation}'\n\nIs the translation correct? Reply briefly: say if it's correct or not, give the right translation if needed, and explain the mistake in Russian."}
        ]
    )
    return message.content[0].text # type: ignore