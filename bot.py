import asyncio
import sys
from chatbot.chatbot import serve_bot
from chatbot.reminder import send_reminders
from chatbot.week_in_review import send_week_in_review_to_all

HELP_MESSAGE = "Runs the bot commands\n\
\n\
Syntax:\n\
bot.py [command]:\n\
\n\
 command:\n\
\n\
 - serve:               Starts the bot and polls new messages\n\
 - send_reminders:      Sends reminder messages to all users that have not\n\
                            written any journal entries in more than a day.\n\
                            This should be executed by a cron-job.\n\
- send_week_in_review:      Sends a summary of the week to all user that have\n\
                            enable_week_in_review flag turned on.\n\
                            This should be executed by a cron-job.\n\
"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        match command:
            case "serve":
                serve_bot()
            case "send_reminders":
                asyncio.run(send_reminders())
            case "send_week_in_review":
                asyncio.run(send_week_in_review_to_all())

            case _:
                print(HELP_MESSAGE)
    else:
        print(HELP_MESSAGE)
