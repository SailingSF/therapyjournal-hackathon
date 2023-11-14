from .open_ai_tools import get_open_ai_client
import time

THERAPIST_ASSISTANT_INSTRUCTIONS = "You are an assistant to a therapist. When asked to analyze a journal entry know that this was from a patient of a therapist and they were asked to write a journal entry with a specific goal in mind. Summarize the journal entry and provide any key insights from the journal. Then after providing that information ask if the therapist would like to update their patient's therapy goals with a suggested new goal."
THERAPIST_ASSISTANT_ID = "asst_yf4eHqUXp7D675OJn6OKGFqt"
THERAPIST_THREAD_ID = "thread_QnCO5ox3kFlifSyMWvl9t7ux"


def analyze_journal(user, journal_entry):
    open_ai_client = get_open_ai_client()
    # add message to analyze the given journal entry

    content = (
        f"Analyze the following journal entry written by a patient: {journal_entry}"
    )

    message = open_ai_client.beta.threads.messages.create(
        thread_id=THERAPIST_THREAD_ID,
        role="user",
        content=content,
    )

    # run therapy assistant with new message
    run = open_ai_client.beta.threads.runs.create(
        thread_id=THERAPIST_THREAD_ID,
        assistant_id=THERAPIST_ASSISTANT_ID,
        instructions=THERAPIST_ASSISTANT_INSTRUCTIONS,
    )

    # wait for run to complete
    while run.status != "completed":
        # print(run)
        run = open_ai_client.beta.threads.runs.retrieve(
            thread_id=THERAPIST_THREAD_ID, run_id=run.id
        )
        time.sleep(2)

    # get messages to print out response for therapist
    messages = open_ai_client.beta.threads.messages.list(thread_id=THERAPIST_THREAD_ID)
    assistant_prompt_text = messages.data[0].content[0].text.value
    return assistant_prompt_text
