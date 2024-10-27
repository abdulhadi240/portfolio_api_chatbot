from fastapi import FastAPI, Depends
from typing import Annotated
import openai
import time
from pydantic import BaseModel
from functions.create_thread import create_thread
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)
app: FastAPI = FastAPI()

assistant_id = "asst_C0dvezXhFksAKE1HfeY4WX7i"

class Chat(BaseModel):
    thread: str
    user_query : str


@app.post('/start')
def create_conversation(thread: Annotated[str, Depends(create_thread)]):
    return {"message": {thread}}


@app.post('/chat')
def chat_with_assistant(chat_request: Chat):
    thread_id = chat_request.thread
    user_input = chat_request.user_query

    if not thread_id:
        return {"error": "Missing thread_id"}, 400

    # Add the user's message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # Run the Assistant
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions=""
    )

    # Poll the assistant for a response
    while True:
        time.sleep(5)

        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        # If run is completed, get the assistant's response
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            assistant_response = None
            for msg in messages.data:
                if msg.role == "assistant":
                    assistant_response = msg.content[0].text.value
                    break
            return {"assistant_response": assistant_response}

        else:
            print("Waiting for the Assistant to process...")
            time.sleep(5)
        
