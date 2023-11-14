from dotenv import load_dotenv
from os import getenv
import time

from .open_ai_tools import get_open_ai_client

load_dotenv()

JOURNAL_ASSISTANT_ID = "asst_McmWR4bMGadmmQAcMxyIbar6"
GENERAL_INSTRUCTIONS = "Please prompt the user to write a journal entry the user as {name}. The user's current therapy goal is '{goal}.' The user has a premium account. Response should be short"


async def get_reminder_message(user, thread):
    open_ai_client = get_open_ai_client()
    specific_instructions = GENERAL_INSTRUCTIONS.format(
        name=user.first_name, goal=user.goal
    )

    # run initial chat
    # journal reminder prompt
    message = open_ai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Remind me to write a journal entry and why right now is a good time.",
    )

    run = open_ai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=JOURNAL_ASSISTANT_ID,
        instructions=specific_instructions,
    )
    while run.status != "completed":
        # print(run)
        run = open_ai_client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        time.sleep(2)

    # print message to prompt journal entry
    messages = open_ai_client.beta.threads.messages.list(thread_id=thread.id)
    assistant_prompt_text = messages.data[0].content[0].text.value
    return assistant_prompt_text
