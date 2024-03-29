# Generated by Django 4.2.1 on 2023-09-05 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0002_cluster_commodity'),
        ('farm', '0003_farm_cluster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='cluster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='farms', to='cluster.cluster'),
        ),
    ]
