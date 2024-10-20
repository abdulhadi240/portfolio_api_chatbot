from fastapi import FastAPI, Depends
from typing import Annotated
import openai
import time
import yfinance as yf
from pydantic import BaseModel
from functions.stock import get_stock_price
from functions.create_thread import create_thread
import json
import os
from dotenv import load_dotenv
from functions.get_menu_items import get_menu_items

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)
app: FastAPI = FastAPI()

assistant_id = "asst_DyEVGMGNaMqPUfdnwQ6KUiAY"

class Chat(BaseModel):
    thread: str
    user_query : str

@app.get('/assistant')
def create_assistant():
    tools_object = {
        "type": "function",
        "function": {
            "name": "get_menu_items",
            "description": "Retrieve all the menu items listed",
            "parameters": {}
        }
    }

    assistant = client.beta.assistants.create(
        name="Stock Assistant",
        instructions="You are a stock market assistant that can retrieve the latest closing price of a stock using its ticker symbol",
        tools=[tools_object],
        model="gpt-3.5-turbo"
    )
    return {"assistant_id": assistant.id}


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
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
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

        elif run_status.status == 'requires_action':
            required_actions = run_status.required_action.submit_tool_outputs.model_dump()

            tool_outputs = []
            for action in required_actions["tool_calls"]:
                func_name = action['function']['name']
                arguments = json.loads(action['function']['arguments'])

                # Example function call handling (expand based on your needs)
                if func_name == "get_menu_items":
                    output = get_menu_items()
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": str(output)
                    })

            # Submit tool outputs back to the assistant
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        else:
            print("Waiting for the Assistant to process...")
            time.sleep(5)
        
