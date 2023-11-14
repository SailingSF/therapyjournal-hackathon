import asyncio
import sys
from chatbot.chatbot import serve_bot
from chatbot.reminder import send_reminders

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
"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        match command:
            case "serve":
                serve_bot()
            case "send_reminders":
                asyncio.run(send_reminders())
            case _:
                print(HELP_MESSAGE)
    else:
        print(HELP_MESSAGE)
