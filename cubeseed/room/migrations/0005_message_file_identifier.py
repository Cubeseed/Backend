# Generated by Django 4.2.1 on 2023-11-22 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_message_multimedia_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file_identifier',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
