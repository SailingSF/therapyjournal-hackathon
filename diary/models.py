from datetime import datetime
from django.db import models


class User(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    thread_id = models.CharField(max_length=50)
    goal = models.CharField(max_length=20000, null=True)
    enable_week_in_review = models.BooleanField(default=False)
    enable_reminders = models.BooleanField(default=False)


class Message(models.Model):
    class AuthorType(models.TextChoices):
        USER = "User"
        JOURNAL_BOT = "JournalBot"
        THERAPIST_BOT = "TherapistBot"

    class SourceType(models.TextChoices):
        TELEGRAM_TEXT = "TelegramText"
        TELEGRAM_VOICE = "TelegramVoice"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    text = models.CharField(max_length=20000)
    created_date = models.DateTimeField(default=datetime.now)
    author = models.CharField(
        max_length=15,
        choices=AuthorType.choices,
        default=AuthorType.USER,
    )
    processed = models.BooleanField(default=False)
    telegram_message_id = models.BigIntegerField(null=True)
    source = models.CharField(
        max_length=15,
        choices=SourceType.choices,
        default=SourceType.TELEGRAM_TEXT,
    )
