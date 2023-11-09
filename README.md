# OpenAI EMERGENCY Hackathon 🚨🚨🚨

# Therapy Journal Assistant

## Idea

Utilizing OpenAI Assistant API we are building a tool to help therapists and patients alike in benefiting from mindful journaling. This project has a list of customers with the ability to add additional customers and will create or run threads with an OpenAI Assistant in order to prompt them to journal. The message sent by the AI to journal will be custom and based on the user's goals in therapy.

Once the user responds with a journal entry this is added to the messages with the AI assistant for added context.

This journal entry will also be analyzed by a different OpenAI Assistant in order to create a summary and create a custom shorter notification for the therapist to read immediately.

The therapist can then update the user's therapy goals so that the next journaling prompt from the assistant will be more personal and accurate.

## How To Use

All code is python and interface is the terminal.

To add a new patient run `python create_patient` which will prompt for the required fields to create a new patient.

To run the program for a specific patient run `python assistant_test.py`. Follow the prompt to enter the `user_id` of the patient you want the assistant to prompt for a journal entry.



Hackathon project to build an OpenAI assistant to aid in therapy patients journaling
