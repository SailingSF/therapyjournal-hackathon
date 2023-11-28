# Therapy Journal AI Assistant

## OpenAI EMERGENCY Hackathon 🚨🚨🚨

## Idea

Utilizing OpenAI Assistant API we are building a tool to help therapists and patients alike in benefiting from mindful journaling. This project has a list of customers with the ability to add additional customers and will create or run threads with an OpenAI Assistant in order to prompt them to journal. The message sent by the AI to journal will be custom and based on the user's goals in therapy.

Once the user responds with a journal entry this is added to the messages with the AI assistant for added context.

This journal entry will also be analyzed by a different OpenAI Assistant in order to create a summary and create a custom shorter notification for the therapist to read immediately.

The therapist can then update the user's therapy goals so that the next journaling prompt from the assistant will be more personal and accurate.

## How To Use

All code is python and interface is the terminal.

### Setup

The therapy journal relies on having OpenAI 'Assistants' to prompt a user and store their journal context. The setup to create these assistantants is shown in the Jupyter Notebook 'assistant_creation.' Assistants can also be created in the [OpenAI Platform UI](https://platform.openai.com/assistants). Once assistants are created, the Assistant_id will need to be saved in the config.json file so that the code is looking at your assistants.

Your OpenAI API key will need to be in the .env file, a sample is given here.

The code takes care of creating new threads for users but those are stored in the patients.json file once created.

The python packages used are all in the requirements.txt file.

### Running Locally

As an example and a demo you can run the agent interaction locally without the telegram bot to see how the assistants work and how the interaction between a patient/user and the assistant as well as how a professional therapist can use the system.

To add a new patient run `python create_patient` which will prompt for the required fields to create a new patient.

To run the program for a specific patient run `python assistant_test.py`. Follow the prompt to enter the `user_id` of the patient you want the assistant to prompt for a journal entry. The program finds if the user has a thread with the journaling assistant and creates one if they don't.
The program then writes to the user using their therapy goal and recent context in the thread to ask for a journaling prompt. The assistant is given instructions on how to ask for that journal entry by using the context of the user saved in the patients.json file and their thread history with the assistant. The user can then submit their journal entry.
Once the journal entry is submitted, it is made part of the thread history with that assistant as well as sent to another assistant for the therapist.
The therapist assistant then summarizes that journal entry, acknowledges the context for that particular user, and suggests an update to that user's therapy goals. If the therapist decides to update the therapy goals at that moment the goals are then updated in the patient.json file and the next time the user is requested to journal it will use that goal as context.

### Running the telegram bot

The telegram bot integration allows easy interaction with the assistant AI from any mobile device, tablet, desktop or via web. The bot requires to set up a new bot on telegram, a postgres database, and the message processing worker.

#### 1. Telegram bot setup

Telegram has a dedicated chatbot that can be used to create new bots, called @BotFather.

1. Open telegram and search for @BotFather
2. write `/newbot` and follow the steps, choosing a name for the bot
3. use the `/token` command to obtain a token and save it in the .env file as `TELEGRAM_BOT_TOKEN=`

#### 2. Postgres setup

You can use any postgres database hosting provider. One thing to be careful with is that many free providers (e.g. https://neon.tech/, will remotely cancel connections after a few minutes, which makes them not a good choice to run in production). A good choice is herokus postgres provider, which costs ca 5usd/month and does not time-out connections.

After choosing a provider and setting up a new server, follow these steps locally.

1. configure the `DATABASE_URL` value in the `.env` file. The url should looks like this `DATABASE_URL="postgres://username:password@ec2-0-0-0-0.compute-1.amazonaws.com:5432/databasename"`
2. create a new virtual env and activate

```
python -m venv venv && source venv/bin/activate
```

3. run database migrations to create the schema

```
python manage.py migrate
```

#### 3. Message processing worker

Do processing worker can be started by using the following command

```
python bot.py serve
```

Now you can use your bot by adding it on telegram and writing `/start`

#### Running the bot in production

The repository is pre-configured to run for production on heroku. In order to run the message worker on heroku:

1. Create a new heroku account and project
2. Under `Dyno Formation` configure a new dyno with the startup command `python bot.py serve`
3. In Settings -> Config Vars configure the environment variables from your local `.env` file.
4. install the [heroku cli](https://devcenter.heroku.com/articles/heroku-cli) and follow the setup steps.
5. Under Deploy -> Deployment method select `Heroku Git` and add the remote to your local repo via

```
git remote add heroku [heroku git url]
```

6. Push the repo to heroku `git posh heroku main`
7. Activate the workers

```
scripts/workers_on
```

Please be aware that you can only run the worker locally OR on heroku, not both at the same time. If you have the worker running on heroku and you would like test something locally, first turn the remote worker off.

```
script/workers_off
```

## Technical Notes

This project uses the new OpenAI Assistants API in order to generate AI model responses with custom instructions and to have context with different users. I personally hadn't paid for the OpenAI API before (never exceeded the credits I had) so I didn't have access to GPT-4 as the AI model underlying the assistants. Undoubtedly that would make the AI generated text better but as this is a proof of concept, GPT3.5 works fine.

The Jupyter Notebooks here were used just to test certain things and to create the OpenAI Assistants. Work can be seen there but the project does not use them.

The patients.json file houses all patient information and is updated when needed.

The config.json file has the relevant Assistant and thread IDs for this program that are general and can be swapped were different assistants made. That file also contains the general instruction prompts for the assistants and can be changed there if prompts are needed to be changed.

## Future work

A frontend will be important to make this more useful as well as a more secure way to handle data than local json files. This can be accomplished in a number of ways and we currently have a telegram bot to accomplish this.
An interface for therapists to analyze all of a patient's journal entries would be great too. Storing the posts both in a traditional database as well as a vector database so that RAG could be done by the AI assistant for the therapist would be a great way to summarize and notice trends through time as well as identify recurring themes.
