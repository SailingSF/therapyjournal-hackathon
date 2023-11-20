from openai import OpenAI
import time

client = OpenAI()

# functions for managing openai assistants

# handling of assistants with "function" tool

# add functions for all assistant "functions" here

# add message to thread
def add_message(message: str, thread_id: str, assistant_id: str):
    '''
    Take message and add it to the assistant's thread
    '''
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )
    return

# run thread with instructions
def run_thread(instructions: str, thread_id: str, assistant_id: str):
    '''
    Run thread with instructions, returns the run id
    '''
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions
    )
    return run.id

# wait for status
def runstatus_handle(run_id: str, thread_id: str, assistant_id: str):
    '''
    Check the status of a run and handle requirements
    '''
    run = client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=run_id)

    while run.status != 'completed':
        if run.status == 'requires_action':
            # find the function and do it
            pass
        else:
            time.sleep(1)

    return
# run based on status
