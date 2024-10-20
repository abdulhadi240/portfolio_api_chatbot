import openai

api_key = "sk-bwq6F1VjDiipTnAmSjNQbQ5w7fhl9TGhUZpejYOiLNT3BlbkFJ2yhicBsobmXIa-jWus2TAVBrr52D9YxojRyuKAv4cA" 

client = openai.OpenAI(api_key=api_key)


def create_thread() -> str:
    thread = client.beta.threads.create()
    return thread.id