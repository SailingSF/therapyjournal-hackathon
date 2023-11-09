import openai as OpenAI
import requests
import json

client = OpenAI()

user_id = input("What is the User ID? ")

# get user goal
with open('patients.json', 'r') as file:
    user_data = json.load(file)

for user in user_data:
    if user['patient_id'] == user_id:
        user_goal = user['data']['contextual_information']['therapy_goals']

initial_instructions = f"You help therapy patients remember to journal about their mental state. Nudge the user to journal about their past week, their stated goals are: {user_goal}"

# access context

# from context create prompt to journal

# respond to journal prompt

# store journal? Keep in thread?

def main():



if __name__ == "__main__":
    main()