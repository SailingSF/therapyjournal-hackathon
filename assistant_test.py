import openai as OpenAI
import requests
import json
import patient_update as pu

client = OpenAI()

user_id = input("What is the User ID? ")

# get user goal file
def get_users():

    with open('patients.json', 'r') as file:
        user_data = json.load(file)
    return user_data

# access context from user file

for user in user_data:
    if user['patient_id'] == user_id:
        user_goal = user['data']['contextual_information']['therapy_goals']

# from context create prompt to journal

initial_instructions = f"You help therapy patients remember to journal about their mental state. Nudge the user to journal about their past week, their stated goals are: {user_goal}"

# start or find thread function
def create_thread(user_id: int):
    '''
    Creates a thread for the given user on the current OpenAI Assistant
    '''
    thread = client.beta.threads.create()
    
    pu.update_threadid(thread.id)

    return thread


def find_thread(user_id: int):
    '''
    Takes a user id parameter and finds the thread on this program's OpenAI Assistant for that user
    If the user does not have a thread it creates one
    '''
    patients = get_users()
    
    for user in patients:
        if user['patient_id'] == user_id:
            try:
                thread_id = user['data']['openai_assistant']['thread_id']
                thread = client.beta.threads.retrieve(thread_id)
            except:
                thread = create_thread(user_id)
    return thread

def main():
    # start new or find thread

    # generate reminder prompt from thread

    # store response

    # analyze resonpse

    # update context

    return



if __name__ == "__main__":
    main()