# Generated by Django 5.0.7 on 2025-03-26 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myChatbot', '0002_rename_session_chathistory_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chathistory',
            name='session_id',
            field=models.ForeignKey(db_column='session_id', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='myChatbot.chatsession'),
        ),
    ]
