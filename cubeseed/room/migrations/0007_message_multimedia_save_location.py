# Generated by Django 4.2.1 on 2023-11-27 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0006_message_multimedia_url_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='multimedia_save_location',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
