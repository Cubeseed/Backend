# Generated by Django 4.2.1 on 2023-10-19 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_waybill_receipt', '0006_alter_invoice_delivered_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='signature',
            field=models.ImageField(upload_to='signatures/'),
        ),
    ]
