# Generated by Django 4.2.1 on 2023-09-27 13:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_orders', '0001_initial'),
        ('farm_planner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('completed', 'Completed')], max_length=20)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase_orders.purchaseorder')),
            ],
        ),
        migrations.AddField(
            model_name='farmplanner',
            name='order_tracker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='farm_planner.ordertracker'),
        ),
    ]
