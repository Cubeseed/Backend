# Generated by Django 4.2.1 on 2023-08-29 19:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        (
            "address",
            "0002_alter_address_osm_checked_alter_address_osm_latitude_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="address",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]