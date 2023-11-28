from diary.models import User
from telegram.ext import (
    ContextTypes,
)


async def telegram_message(
    user: User, context: ContextTypes.DEFAULT_TYPE, message: str
):
    await context.bot.send_message(
        chat_id=user.chat_id,
        text=message,
    )
