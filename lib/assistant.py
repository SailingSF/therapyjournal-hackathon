from dotenv import load_dotenv
from os import getenv
import time

from lib.threads import create_thread

from .open_ai_tools import get_open_ai_client

load_dotenv()

JOURNAL_ASSISTANT_ID = "asst_McmWR4bMGadmmQAcMxyIbar6"
GENERAL_INSTRUCTIONS = "Please prompt the user to write a journal entry the user as {name}. The user's current therapy goal is '{goal}.' The user has a premium account. Response should be short"
SUMMARY_ASSISTANT_ID = "asst_IFlu8xBgOugca8SEFjUax2lK"
RETRO_ASSISTANT_ID = "asst_5VFsiTgOoMpVf4oUIMuDHiiH"


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


async def summarize_week(user, journal_entries):
    open_ai_client = get_open_ai_client()

    journal_entries_text = ""
    async for message in journal_entries:
        journal_entries_text += (
            f"<entry>{message.created_date.isoformat()} {message.text}</entry>\n\n"
        )
    thread = create_thread(user, open_ai_client)

    message = open_ai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=journal_entries_text,
    )

    # run therapy assistant with new message
    run = open_ai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=SUMMARY_ASSISTANT_ID,
        instructions=f"Start the message saying 'Hey [name], this is your week in review:'. Their name is '{user.first_name}'",
    )

    # wait for run to complete
    while run.status != "completed":
        # print(run)
        run = open_ai_client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        time.sleep(2)

    # get messages to print out response for therapist
    messages = open_ai_client.beta.threads.messages.list(thread_id=thread.id)
    assistant_prompt_text = messages.data[0].content[0].text.value
    return assistant_prompt_text


def suggest_improvements(user, challenge, diary_entries):
    open_ai_client = get_open_ai_client()
    thread = create_thread(user, open_ai_client)

    message = open_ai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"These are the journal entries for this user for the past week: \n\
<START OF JOURNEY ENTRIES>\n\
{diary_entries}\n\
<END OF JOURNEY ENTRIES>\n\
\n\
The user states that this is is current main challenge: {challenge}",
    )

    # run therapy assistant with new message
    run = open_ai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=RETRO_ASSISTANT_ID,
        instructions="Please return the answer in the format of bullet points.",
    )

    # wait for run to complete
    while run.status != "completed":
        # print(run)
        run = open_ai_client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        time.sleep(2)

    # get messages to print out response for therapist
    messages = open_ai_client.beta.threads.messages.list(thread_id=thread.id)
    assistant_prompt_text = messages.data[0].content[0].text.value
    return assistant_prompt_text
