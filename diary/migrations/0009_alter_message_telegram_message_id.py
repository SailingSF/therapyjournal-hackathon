# Generated by Django 4.2.7 on 2023-11-16 23:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0008_alter_user_chat_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="telegram_message_id",
            field=models.BigIntegerField(null=True),
        ),
    ]
