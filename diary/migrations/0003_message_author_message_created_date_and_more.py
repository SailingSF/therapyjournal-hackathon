# Generated by Django 4.2.7 on 2023-11-13 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0002_remove_user_pub_date_remove_user_question_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="author",
            field=models.CharField(
                choices=[
                    ("User", "User"),
                    ("JournalBot", "Journal Bot"),
                    ("TherapistBot", "Therapist Bot"),
                ],
                default="User",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="created_date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="message",
            name="processed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="message",
            name="source",
            field=models.CharField(
                choices=[
                    ("TelegramText", "Telegram Text"),
                    ("TelegramVoice", "Telegram Voice"),
                ],
                default="TelegramText",
                max_length=15,
            ),
        ),
    ]
