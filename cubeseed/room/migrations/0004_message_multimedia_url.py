# Generated by Django 4.2.1 on 2023-10-31 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_remove_message_user_message_from_user_message_read_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='multimedia_url',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
