import json
from datetime import datetime

def create_patient_record():
    # Collect patient information
    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    therapy_goal = input("Enter the patients therapy goal: ")

    # Read current data
    file_name = 'patients.json'
    try:
        with open(file_name, 'r') as file:
            patients = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file does not exist or is empty/invalid, start with an empty list
        patients = []

    try:
        max_id = max((patient['patient_id'] for patient in patients), default=0)
    except:
        max_id = 0
    # Collect new patient information
    patient_id = max_id + 1
    
    # Initialize the patient data structure
    patient_data = {
        "patient_id": patient_id,
        "data": {
            "name": name,
            "age": age,
            "created_at": datetime.now().isoformat(),
            "journal_entries": [],
            "contextual_information": {
                # Add default or empty contextual information as needed
                "therapy_goals": therapy_goal
            }
        }
    }
    if type(patients) == list:
        patients.append(patient_data)
    else:
        a_list = []
        patients = a_list.append(patient_data)
    # Convert the patient data to JSON format
    patient_json = json.dumps(patients, indent=4)


    # Write the JSON data to the file
    with open(file_name, 'w') as file:
        file.write(patient_json)

    print(f"Patient record for {name} has been created and stored in {file_name}, their user id is {patient_id}")


if __name__ == "__main__":
    print("New patient creator")

    create_patient_record()