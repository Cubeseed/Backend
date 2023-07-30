# Generated by Django 4.2.1 on 2023-07-30 04:03

import cubeseed.filedescriptor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0007_farmerprofile_reviewed_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCertificateFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('review_status', models.CharField(choices=[('P', 'PENDING'), ('R', 'REJECTED'), ('A', 'APPROVED')], default='P', max_length=1)),
                ('reviewed_date', models.DateField(blank=True, null=True)),
                ('certificate', models.FileField(upload_to=cubeseed.filedescriptor.models.upload_certificate)),
                ('farmer_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.farmerprofile')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userprofile.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
