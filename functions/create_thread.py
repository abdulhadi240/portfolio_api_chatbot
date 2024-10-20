import openai
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)


def create_thread() -> str:
    thread = client.beta.threads.create()
    return thread.id