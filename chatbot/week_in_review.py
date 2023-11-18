from lib.env import env
from lib.assistant import summarize_week
from asgiref.sync import sync_to_async
from telegram.ext import ApplicationBuilder
from datetime import datetime, timedelta
import db
from diary.models import User


async def send_week_in_review(user, bot):
    messages_last_week = user.messages.filter(
        created_date__gte=datetime.now() - timedelta(weeks=1),
        author="User",
    )

    summary = await summarize_week(user, messages_last_week)

    await bot.send_message(
        chat_id=user.chat_id,
        text=summary,
    )

    message = await sync_to_async(user.messages.create)(
        text=summary,
        author="SummaryBot",
    )


async def send_week_in_review_to_all():
    if datetime.now().weekday() == 4:
        application = ApplicationBuilder().token(env("TELEGRAM_BOT_TOKEN")).build()
        async for user in User.objects.filter(enable_week_in_review=True).all():
            await send_week_in_review(user, application.bot)
