from asgiref.sync import sync_to_async
import logging
from os import getenv
import io
from telegram import Update
import telegram
import datetime
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from chatbot.week_in_review import send_week_in_review

import db
from diary.models import User
from lib.assistant import get_reminder_message, suggest_improvements, summarize_week
from lib.threads import get_or_create_thread
from lib.therapist import analyze_journal
from lib.open_ai_tools import get_open_ai_client
from lib.utils import remove_command_string
from lib.env import env

MIN_MESSAGE_LENGTH_FOR_REFLECTION = 200

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "I am journal bot. \
Write down your journal entries here.\n\n \
\
You can set a personal goal by using the /setgoal command. \n \
Once you wrote something, you can use the /reflect command to get an analysis of your comments.\n\n\
You can see your current goal by using the /goal command, and general info by using the /info command."

    # keyboard = [
    #     [telegram.KeyboardButton("/setgoal time-management")],
    #     [telegram.KeyboardButton("/setgoal work-life balance")],
    # ]
    # keyboard_markup = telegram.ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.message.chat_id, text=text  # , reply_markup=keyboard_markup
    )


async def get_user(update):
    chat_id = update.effective_chat.id
    try:
        user = await sync_to_async(User.objects.get)(chat_id=chat_id)
    except:
        user = await sync_to_async(User.objects.create)(
            chat_id=chat_id, first_name=update.effective_user.first_name
        )
    return user


async def set_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    user.goal = remove_command_string(update.message.text)
    await sync_to_async(user.save)()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Goal updated"
    )


async def new_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    message = await sync_to_async(user.messages.create)(
        user=user,
        text=update.message.text,
        author="User",
        telegram_message_id=update.message.message_id,
        source="TelegramText",
    )


async def reflect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    combined = ""
    async for message in user.messages.filter(author="User", processed=False):
        combined += message.text + "\n\n"
    # async for author in Author.objects.filter(name__startswith="A"):
    #     book = await author.books.afirst()

    if len(combined) < MIN_MESSAGE_LENGTH_FOR_REFLECTION:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Analysis will be more helpful if you write at last {MIN_MESSAGE_LENGTH_FOR_REFLECTION - len(combined)} more characters before reflecting.",
        )
    else:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=telegram.constants.ChatAction.TYPING,
        )

        # Obtain analysis
        analysis = analyze_journal(user, combined)

        # Send to telegram
        telegram_message = await context.bot.send_message(
            chat_id=update.effective_chat.id, text=analysis
        )
        # Archive therapist message
        message = await sync_to_async(user.messages.create)(
            user=user,
            text=analysis,
            author="TherapistBot",
            telegram_message_id=telegram_message.message_id,
        )
        # Mark existing messages as processed
        await sync_to_async(user.messages.filter(author="User").update)(processed=True)


async def get_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your current goal is: {user.goal}",
    )


async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    # collect journal statistics
    message_count = await sync_to_async(user.messages.filter(author="User").count)()
    unprocessed_count = await sync_to_async(
        user.messages.filter(processed=False, author="User").count
    )()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"You have {unprocessed_count} / {message_count} unprocessed journal entries.",
    )


async def transcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    audio_file = await context.bot.get_file(update.message.voice.file_id)
    buffer = io.BytesIO()
    buffer.name = "audiofile.ogg"
    await audio_file.download_to_memory(buffer)
    open_ai_client = get_open_ai_client()
    transcript = open_ai_client.audio.transcriptions.create(
        model="whisper-1", file=buffer, response_format="verbose_json"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Transcription: {transcript.text}",
    )

    message = await sync_to_async(user.messages.create)(
        text=transcript.text,
        author="User",
        telegram_message_id=update.message.message_id,
        source="TelegramVoice",
    )


async def set_challenges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)

    challenges = remove_command_string(update.message.text)

    messages_last_week = user.messages.filter(
        created_date__gte=datetime.datetime.now() - datetime.timedelta(weeks=1),
        author="User",
    )

    combined = ""
    async for message in messages_last_week:
        combined += message.text + "\n\n"

    improvements = await suggest_improvements(user, challenges, combined)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=improvements,
    )

    message = await sync_to_async(user.messages.create)(
        text=improvements,
        author="RetroBot",
    )


async def send_week_in_review_wrapper(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user = await get_user(update)
    await send_week_in_review(user, context.bot)


def serve_bot():
    application = ApplicationBuilder().token(env("TELEGRAM_BOT_TOKEN")).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    set_goal_handler = CommandHandler("setgoal", set_goal)
    application.add_handler(set_goal_handler)

    get_goal_handler = CommandHandler("goal", get_goal)
    application.add_handler(get_goal_handler)

    get_info_handler = CommandHandler("info", get_info)
    application.add_handler(get_info_handler)

    set_reflect_handler = CommandHandler("reflect", reflect)
    application.add_handler(set_reflect_handler)

    set_summarize_handler = CommandHandler(
        "week_in_review", send_week_in_review_wrapper
    )
    application.add_handler(set_summarize_handler)

    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), new_entry)
    application.add_handler(message_handler)

    transcription_handler = MessageHandler(
        filters.VOICE & (~filters.COMMAND), transcribe
    )
    application.add_handler(transcription_handler)

    application.run_polling()
