# Generated by Django 4.2.1 on 2023-09-08 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0005_alter_address_osm_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='local_government_area',
            field=models.CharField(default='Aba North', max_length=50, verbose_name='Local Government Area'),
        ),
    ]
