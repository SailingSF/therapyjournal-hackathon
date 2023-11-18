from diary.models import User
from lib.env import env
from lib.assistant import get_reminder_message
from lib.threads import get_or_create_thread
from asgiref.sync import sync_to_async
from telegram.ext import ApplicationBuilder
from datetime import datetime


async def send_reminder(user, bot):
    thread = await get_or_create_thread(user)
    print("request reminder message")
    reminder_message = await get_reminder_message(user, thread)
    print("got message")
    telegram_message = await bot.send_message(
        chat_id=user.chat_id, text=reminder_message
    )

    await sync_to_async(user.messages.create)(
        text=reminder_message,
        author="JournalBot",
        telegram_message_id=telegram_message.message_id,
    )


async def send_reminders():
    if datetime.now().weekday() != 4:
        application = ApplicationBuilder().token(env("TELEGRAM_BOT_TOKEN")).build()
        async for user in User.objects.all():
            last_message = await sync_to_async(
                user.messages.filter(author="User").order_by("-created_date").first
            )()
            time_ago = datetime.now() - last_message.created_date.replace(tzinfo=None)
            print(f"Time ago for {user.first_name} is {time_ago}")
            if time_ago.days >= 1:
                await send_reminder(user, application.bot)
