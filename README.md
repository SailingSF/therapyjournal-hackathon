# Therapy Journal AI Assistant

## OpenAI EMERGENCY Hackathon 🚨🚨🚨

## Idea

Utilizing OpenAI Assistant API we are building a tool to help therapists and patients alike in benefiting from mindful journaling. This project has a list of customers with the ability to add additional customers and will create or run threads with an OpenAI Assistant in order to prompt them to journal. The message sent by the AI to journal will be custom and based on the user's goals in therapy.

Once the user responds with a journal entry this is added to the messages with the AI assistant for added context.

This journal entry will also be analyzed by a different OpenAI Assistant in order to create a summary and create a custom shorter notification for the therapist to read immediately.

The therapist can then update the user's therapy goals so that the next journaling prompt from the assistant will be more personal and accurate.

## How To Use

All code is python and interface is the terminal.

To add a new patient run `python create_patient` which will prompt for the required fields to create a new patient.

To run the program for a specific patient run `python assistant_test.py`. Follow the prompt to enter the `user_id` of the patient you want the assistant to prompt for a journal entry. The program finds if the user has a thread with the journaling assistant and creates one if they don't.
The program then writes to the user using their therapy goal and recent context in the thread to ask for a journaling prompt. The assistant is given instructions on how to ask for that journal entry by using the context of the user saved in the patients.json file and their thread history with the assistant. The user can then submit their journal entry.
Once the journal entry is submitted, it is made part of the thread history with that assistant as well as sent to another assistant for the therapist.
The therapist assistant then summarizes that journal entry, acknowledges the context for that particular user, and suggests an update to that user's therapy goals. If the therapist decides to update the therapy goals at that moment the goals are then updated in the patient.json file and the next time the user is requested to journal it will use that goal as context.

## Technical Notes

This project uses the new OpenAI Assistants API in order to generate AI model responses with custom instructions and to have context with different users. I personally hadn't paid for the OpenAI API before (never exceeded the credits I had) so I didn't have access to GPT-4 as the AI model underlying the assistants. Undoubtedly that would make the AI generated text better but as this is a proof of concept, GPT3.5 works fine.

The Jupyter Notebooks here were used just to test certain things and to create the OpenAI Assistants. Work can be seen there but the project does not use them.

The patients.json file houses all patient information and is updated when needed.

The config.json file has the relevant Assistant and thread IDs for this program that are general and can be swapped were different assistants made. That file also contains the general instruction prompts for the assistants and can be changed there if prompts are needed to be changed.

## Future work

With the release of GPTs this morning (11/9/23) a lot of this behaviour can be replicated and utilize the chatGPT interface. I built this by experimenting for an hour and hope to improve it and include the multiple roles features of patients and a therapist. <https://chat.openai.com/g/g-dPWBwvrUV-reflection-companion>

A frontend will be important to make this more useful as well as a more secure way to handle data than local json files.
An interface for therapists to analyze all of a patient's journal entries would be great too. Storing the posts both in a traditional database as well as a vector database so that RAG could be done by the AI assistant for the therapist would be a great way to summarize and notice trends through time as well as identify recurring themes.
