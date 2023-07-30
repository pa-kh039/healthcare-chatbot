import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
from conf import OPENAI_API_KEY
from helper import find_nearby_docs

# Load your OpenAI API key
models.OpenAI.api_key = OPENAI_API_KEY
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT =  "You are Ved, a healthcare chatbot. Do not prescribe any medicines. Provide home remedies, exercises, etc. and some possible causes of the medical problem faced by the user. Do not answer any queries not related to health. Do not respond to non-health related topics and tell the user that you are only a healthcare chatbot. Give point-wise response in 4-5 lines. Finally at the end of your response, tell the user to type 'NEARBY-DOCS-{yourPincode}' to know about the healthcare centres near his location."


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """
    usr_inp=((message_history[-1]).content)

    if usr_inp[:12] in ['NEARBY-DOCS-',"nearby-docs-",'Nearby-docs-']:
        # print("expecting an indian pin code in proper format like NEARBY-DOCS-492015")
        pincode=usr_inp[12:18]
        return find_nearby_docs(pincode)
    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )

    return bot_response, state
