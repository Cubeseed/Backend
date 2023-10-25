# Generated by Django 4.2.1 on 2023-10-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_waybill_receipt', '0008_alter_invoice_delivered_to_alter_invoice_sent_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='service',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='service_details',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
