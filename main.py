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
from functions.get_orders_details import get_order_details
from functions.create_customer import create_new_customers
from functions.create_complain import create_new_complain
from functions.create_orders import create_new_order
load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)
app: FastAPI = FastAPI()

assistant_id = "asst_T3zdvY3z9ild1I1GM1LDavG4"

class Chat(BaseModel):
    thread: str
    user_query : str

@app.get('/assistant')
def create_assistant():
    tools_object = [
        {
            "type": "function",
            "function": {
                "name": "get_menu_items",
                "description": "Get all menu details. Call this whenever you need to know the menu related data",
                "parameters": {}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_order_details",
                "description": "Get all orders details. Call this whenever you need to know the order related data",
                "parameters": {}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_new_customers",
                "description": "Creates new order for the customer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "firstname": {
                            "type": "string",
                            "description": "The firstname of the customer"
                        },
                        "lastname": {
                            "type": "string",
                            "description": "The lastname of the customer"
                        },
                        "email": {
                            "type": "string",
                            "description": "The email of the customer"
                        },
                        "phonenumber": {
                            "type": "string",
                            "description": "The phonenumber of the customer"
                        },
                        "date": {
                            "type": "string",
                            "description": "The current date"
                        }
                    },
                    "required": ["firstname", "lastname", "email", "phonenumber", "date"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_new_complain",
                "description": "Check if the user is an exisiting customer . If yes then take email and firstname , and complain else make a new customer and then file the complain",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "firstname": {
                            "type": "string",
                            "description": "The firstname of the customer making the complaint"
                        },

                        "email": {
                            "type": "string",
                            "description": "The email of the customer"
                        },
                        "date": {
                            "type": "string",
                            "description": "The date of the complaint"
                        },
                        "complain": {
                            "type": "string",
                            "description": "The text of the complaint"
                        }
                    },
                    "required": ["firstname", "email", "date", "complain"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_new_order",
                "description": "Check if the user is an exisiting customer . If yes then take email and firstname , and complain else make a new customer and then file the complain",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "**Ask Customer to provide email** Note. (!! Dont write email from your side !!) . Check if the customer is already our member , if yes find out customer id , if no create a new customer by asking edtails from user."
                        },

                        "menuid": {
                            "type": "integer",
                            "description": "The id of the menu item selected be the customer . Dont ask customer for the id , ask for item name and find id yourself"
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "The quantity of the menu item selected by the customer"
                        },
                        "address": {
                            "type": "string",
                            "description": "The address at which items should be delivered. Ask Customer to provide address** Note. (!! Dont write address from your side !!)"
                        },
                        "instruction": {
                            "type": "string",
                            "description": "The instruction of the menu item selected by the customer. Ask Customer to provide instructions** Note. (!! Dont write instructions from your side !!)"
                        },
                        "date": {
                            "type": "string",
                            "description": "The date of the complaint.Dont ask customer for the date . use current date."
                        }
                    },
                    "required": ["email", "menuid", "quantity", "address","instruction","date"]
                }
            }
        }
]


    assistant = client.beta.assistants.create(
        name="Resturant Customer Service",
        instructions="""Standard Operating Procedure (SOP) for Laziz Catering Services LLC
Document Control
Document Title: Laziz Catering Services LLC Overview and Operations
1. Purpose
The purpose of this SOP is to provide a structured approach for communicating the key offerings, services, and operational procedures of Laziz Catering Services LLC, ensuring consistency, professionalism, and clarity in all customer interactions and event planning processes.

2. Scope
This SOP applies to all staff involved in client communications, event planning, culinary execution, and service delivery for Laziz Catering Services LLC. It serves as a guide for both front-end and back-end operations, ensuring seamless service and consistent brand representation.

3. Responsibilities
Catering Manager: Oversees the overall operations, ensuring that all processes adhere to the SOP.
Chefs & Kitchen Staff: Responsible for food preparation, menu planning, and maintaining quality standards.
Customer Service Representatives: Handle client inquiries, bookings, and feedback.
Event Coordinators: Plan and execute events, ensuring a smooth experience for the client.
Service Staff: Ensure flawless service during events and maintain professionalism.
4. Procedure
4.1. Welcome Process
Objective: To create a warm and professional first impression for every client.
Procedure:
When a new client contacts Laziz Catering, respond promptly within 15 minutes (via email, call, or message).

Use the following welcome note template:

"We are thrilled to bring exceptional culinary experiences to your events in Dubai, blending international flavors with local influences. Trust us to make your occasion unforgettable with our creative menus and impeccable service. Welcome to Laziz Catering, A Taste of Home Away from Home!"

Ensure the client feels valued and introduce the range of services offered by Laziz Catering.

4.2. About Us Presentation
Objective: To accurately present Laziz Catering’s mission, vision, and capabilities.
Procedure:
Use the following key message when discussing the company with clients:

"Welcome to Laziz Catering, your premier partner for exceptional culinary experiences in the heart of Dubai. Whether it’s an intimate gathering or a lavish wedding, our chefs craft menus using fresh, high-quality ingredients with a fusion of international and local flavors, ensuring a seamless and memorable event experience."

Emphasize Laziz Catering’s commitment to excellence, creativity, and impeccable service during conversations.

4.3. Service Offering and Execution
Objective: To deliver exceptional culinary services, from menu planning to event execution.

Procedure:

Menu Planning: Collaborate with clients to create a tailored menu based on their preferences, cultural needs, and dietary restrictions.
Tastings: Offer clients tastings to ensure the menu meets their expectations.
On-Site Execution: The catering team must arrive at least 2 hours before the event to set up and prepare. All dishes should be freshly prepared on-site when possible to ensure quality.
Post-Event Clean-Up: Ensure that the event site is left clean and tidy.
Key Service Points:

Use the finest fresh ingredients to ensure a memorable gastronomic journey.
Focus on meticulous planning and execution, ensuring the event is stress-free for clients.
4.4. Vision and Mission
Vision Statement:
"At Laziz Catering, we aspire to redefine culinary experiences in Dubai by blending international flavors with local influences. We aim to surpass expectations and leave a lasting impression on you and your guests."

Mission Statement:
"Our mission is to deliver culinary experiences that transcend the ordinary. Using the finest ingredients, we craft dishes designed to delight and surpass your expectations, providing impeccable service and unforgettable memories."

4.5. Team Introduction
Objective: To present a professional and creative team to clients, building trust.
Procedure:
Introduce the team by emphasizing their professionalism, experience, and dedication to excellence. Use the following description:

"Our expert team, from talented chefs to attentive servers, combines passion with professionalism to ensure your event is a success. With precision and warm hospitality, we bring your vision to life."

4.6. Client Interaction and Feedback Collection
Objective: To ensure high client satisfaction through professional communication and consistent feedback collection.
Procedure:
Client Interaction:
Maintain a polite, professional, and helpful demeanor in all client communications.
Feedback Collection:
After each event, ask clients for feedback using a standardized questionnaire.
Record both positive and negative feedback and discuss improvements with the team weekly.
4.7. Marketing and Global Presence
Objective: To showcase Laziz Catering’s renown beyond Dubai and build a global reputation.
Procedure:
Highlight Laziz Catering’s international appeal by featuring unique dishes and fusion recipes that attract visitors from around the world.
Emphasize Laziz Catering’s online presence for purchasing signature sauces and spices.
Update the food gallery regularly with high-quality images of dishes that reflect international and local culinary influences.
4.8. Daily Visitor Statistics
Objective: Track and analyze visitor flow to continuously improve services.
Procedure:
Use visitor tracking tools to monitor daily website traffic and inquiries.
Report on visitor trends and customer demographics weekly.
4.9. Contact Information Handling
Objective: Provide clients with accurate and accessible contact details.
Procedure:
Ensure that the following contact details are included in all communications and promotional materials:

Address:
Bin Haider Warehouse Complex, Warehouse No. 12, Dubai Investment Park-2, Jabel Ali, Dubai, UAE
Email: [Insert Email]
Phone Numbers:
+971 56 192 3426
+971 56 421 9775
+971 56 171 2232

5. Quality Control
Client Satisfaction: Regularly check client feedback to ensure high service standards are being met.
Food Quality: Ensure that all ingredients meet Laziz Catering’s quality standards, with a focus on freshness and safety.
Event Execution: Conduct routine assessments of event planning and execution, ensuring flawless delivery.
6. Review and Continuous Improvement
This SOP will be reviewed every 6 months to ensure all procedures remain relevant and effective.
Feedback from clients and staff will be taken into account to make necessary adjustments to enhance operational efficiency and service quality.
This SOP should be followed by all staff members to ensure that Laziz Catering delivers consistent, high-quality services that exceed client expectations.""",
        tools=tools_object,  # Pass tools as an object
        model="gpt-4-turbo"
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

                if func_name == "get_menu_items":
                    output = get_menu_items()
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": str(output)
                    })
                elif func_name == "get_order_details":
                        output = get_order_details()
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": str(output)
                        })
                elif func_name == "create_new_customers":
                        output = create_new_customers(
                            arguments['firstname'],
                            arguments['lastname'],
                            arguments['email'],
                            arguments['phonenumber'],
                            arguments['date'],
                        )
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": str(output)
                        })
                elif func_name == "create_new_complain":
                        output = create_new_complain(
                            arguments['firstname'],
                            arguments['email'],
                            arguments['date'],
                            arguments['complain'],
                        )
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": str(output)
                        })
                elif func_name == "create_new_order":
                        output = create_new_order(
                            arguments['email'],
                            arguments['menuid'],
                            arguments['quantity'],
                            arguments['address'],
                            arguments['instruction'],
                            arguments['date'],
                            
                        )
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": str(output)
                        }) 
                               
                else:
                  raise ValueError(f"Unknown function: {func_name}")
                   

            # Submit tool outputs back to the assistant
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        else:
            print("Waiting for the Assistant to process...")
            time.sleep(5)
        
