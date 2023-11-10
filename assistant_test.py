import re
from openai import OpenAI
import os
import requests
import json
import patient_update as pu
import time

# lord forgive me for global variables 🙏
client = OpenAI()

configfile_name = 'config.json'
patientsfile_name = 'patients.json'

# get user goal file
def get_json_file(filename):
# opens specified json file and returns dictionary
    with open(filename, 'r') as file:
        user_data = json.load(file)
    return user_data

# access context from user file

def get_user_data(user_id: int):
# gets data for single user based on user id
    patients = get_json_file(patientsfile_name)
    for user in patients:
        if user['patient_id'] == user_id:
            return user

def create_thread(user_id: int):
    '''
    Creates a thread for the given user on the current OpenAI Assistant
    Used when a user does not have an active thread with an Assistant
    '''
    thread = client.beta.threads.create()
    
    # save thread_id to user so further interactions use the correct thread
    pu.update_threadid(user_id, thread.id)

    return thread


def find_thread(user_id: int):
    '''
    Takes a user id parameter and finds the thread on this program's OpenAI Assistant for that user
    If the user does not have a thread it calls the create thread function
    '''
    patients = get_json_file(patientsfile_name)

    for user in patients:
        if user['patient_id'] == user_id:
            # try to find thread for user, if no thread it creates one
            try:
                thread_id = user['data']['openai_assistant']['thread_id']
                thread = client.beta.threads.retrieve(thread_id)
                print('Existing thread found')
            except:
                print('Creating new thread')
                thread = create_thread(user_id)
                print(f"New thread created with id: {thread.id}")

    return thread

def run_chat(thread_id, instructions):
    '''
    Runs specific thread with assistant and instructions
    '''

def request_journal_entry(user_id: int):
    '''
    Logic to ask the patient for a journal entry
    '''
    user = get_user_data(user_id)
    # get thread
    thread = find_thread(user_id)

    # set instruction based on goal
    user = get_user_data(user_id)
    user_goal = user['data']['contextual_information']['therapy_goals']
    name = user['data']['name']
    general_instructions = get_json_file(configfile_name)['journal_assistant_instructions']
    specific_instructions = general_instructions.format(name=name, goal=user_goal)


    # run initial chat
        # journal reminder prompt
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Remind me to write a journal entry and why right now is a good time."
    )

    journal_assistant_id = get_json_file(configfile_name)['journal_assistant_id']

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=journal_assistant_id,
    instructions=specific_instructions
    )
    while run.status != 'completed':
        print(run)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
        time.sleep(2)


    # print message to prompt journal entry
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_prompt_text = messages.data[0].content[0].text.value
    print(assistant_prompt_text)

    journal_entry = input("Input: ")

    # add journal to thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=journal_entry
    )

    return journal_entry

def analyze_entry(journal_entry, user_id):
    '''
    Looks at most recent journal entry from patient with a separate AI Assistant
    Creates summary with analysis for therapist
    Uses AI assistant with custom instruction to ask for analysis and goal update
    Shares analysis with therapist and gives the option to update the therapy goal which is then saved in the patient file.
    The updated therapy goal will then be used on further assistant/patient interactions
    '''
    # get openai assistant params specific to the therapist assistant
    assistant_id = get_json_file(configfile_name)['therapist_assistant_id']
    thread_id = get_json_file(configfile_name)['therapist_thread_id']

    # get information about relevant user
    user = get_user_data(user_id)
    current_goal = user['data']['contextual_information']['therapy_goals']
    name = user['data']['name']

    # add message to analyze the given journal entry
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=f"Analyze the following journal entry written by a patient: {journal_entry}"
    )

    # get the instructions for the therapy assistant
    general_instructions = get_json_file(configfile_name)['therapist_assistant_instructions']

    # run therapy assistant with new message
    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions=general_instructions
    )

    # wait for run to complete
    while run.status != 'completed':
        print(run)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=run.id)
        time.sleep(2)


    # get messages to print out response for therapist
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_prompt_text = messages.data[0].content[0].text.value
    print(assistant_prompt_text)

    # create new therapy goal if needed
    make_new_goal = input(f"Would you like to update {name}'s therapy goal? Their current goal is {current_goal}. Y/n  ")
    if make_new_goal.upper() == 'Y':
        new_therapy_goal = input("New therapy goal:  ")
        pu.update_goal(user_id, new_therapy_goal)

    else:
        print(f"Keeping current goal of {current_goal}")

    return


def main():
    # get user who will be asked for a journal entry
    user_id = int(input("What is the User ID? "))
    
    # get journal entry for user from context (lots of other stuff happens here too)
    journal_entry = request_journal_entry(user_id)
    
    # store response securely (TODO)

    # analyze resonpse with separate AI Assistant and suggest an updated goal (and other stuff)
    analyze_entry(journal_entry, user_id)

    return



if __name__ == "__main__":
    main()