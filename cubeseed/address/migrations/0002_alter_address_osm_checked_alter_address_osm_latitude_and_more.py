# Generated by Django 4.2.1 on 2023-08-28 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("address", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="osm_checked",
            field=models.BooleanField(
                default=False, verbose_name="Checked by Open Street Map API"
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="osm_latitude",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="osm_longitude",
            field=models.FloatField(null=True),
        ),
    ]
