import re
from openai import OpenAI
import os
import requests
import json
import patient_update as pu
import time

client = OpenAI()

configfile_name = 'config.json'
patientsfile_name = 'patients.json'



# get user goal file
def get_json_file(filename):
# opens patients json file and returns dictionary
    with open(filename, 'r') as file:
        user_data = json.load(file)
    return user_data

# access context from user file

def get_user_data(user_id: int):
# gets goal text from user data
    patients = get_json_file(patientsfile_name)
    for user in patients:
        if user['patient_id'] == user_id:
            return user


# start or find thread function
def create_thread(user_id: int):
    '''
    Creates a thread for the given user on the current OpenAI Assistant
    '''
    thread = client.beta.threads.create()
    
    pu.update_threadid(user_id, thread.id)

    return thread


def find_thread(user_id: int):
    '''
    Takes a user id parameter and finds the thread on this program's OpenAI Assistant for that user
    If the user does not have a thread it creates one
    '''
    patients = get_json_file(patientsfile_name)

    print(f"Getting thread from user file for user id: {user_id}")

    for user in patients:
        if user['patient_id'] == user_id:
            print('found user')
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
    if run.status != 'completed':
        print(run)
        time.sleep(2)
    else:
        pass

    # print message to prompt journal entry
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_prompt_text = messages.data[0].content[0].text.value
    print(assistant_prompt_text)


    # respond to journal entry
        # confirm chat is journal entry?
        
    # end

def analyze_entry():
    '''
    Looks at most recent journal entry from patient
    Creates summary with analysis for therapist
    Uses completion API (for now) to get analysis of single entry
    Shares analysis with therapist
    '''

def update_goal():
    '''
    Ask therapist if goal should be updated
    Suggests new goal first, asks if ok
    Updates goal in patients.json
    '''



def main():
    user_id = int(input("What is the User ID? "))
    # start new or find thread

    # generate reminder prompt from thread
    request_journal_entry(user_id)
    # store response

    # analyze resonpse

    # update context

    return



if __name__ == "__main__":
    main()