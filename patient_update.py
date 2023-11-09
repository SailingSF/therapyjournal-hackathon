import json

# functions to help update user info

def get_patients_file():
    '''
    Gets the local patients file to read in as a oython dictionary
    '''

    with open('patients.json', 'r') as file:
        json_file = json.load(file)
    
    return json_file

def save_patients_file(patients):
    '''
    Takes python dictionary of patients file and saves it back to location
    '''
    # Convert the patient data to JSON format
    patient_json = json.dumps(patients, indent=4)

    # Write the JSON data to the file
    with open('patients.json', 'w') as file:
        file.write(patient_json)


def update_thread(user_id: int, thread_id: str):
    '''
    Updates patients.json for the given user id with the thread id for that user
    '''
    patients = get_patients_file()

    for user in patients:
        if user['patient_id'] == user_id:
            user['data']['openai_assistant']['thread_id'] = thread_id
    
    save_patients_file(patients)

    return