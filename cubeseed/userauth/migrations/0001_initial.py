"""Initial migration"""
# Generated by Django 4.2.1 on 2023-05-31 17:00
#pylint:disable=invalid-name
from django.db import migrations
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.management import create_permissions

MODERATOR = "moderator"
FARMER = "farmer"
BUYER = "buyer"
INVESTOR = "investor"
INPUT = "input"
SERVICE = "service"
PROCESSOR = "processor"


def create_initial_data():
    """Create groups and superuser"""
    group_names = [
        MODERATOR,
        FARMER,
        BUYER,
        INVESTOR,
        INPUT,
        SERVICE,
        PROCESSOR,
    ]
    groups = []
    for name in group_names:
        groups.append(Group.objects.create(name=name))

    User.objects.create_superuser(
        username="admin",
        email="superadmin@fake.com",
        password="admin123",
    ).groups.set(groups)


def add_permissions(apps):
    """
    make sure default permissions are created, see
    https://stackoverflow.com/questions/38822273/how-to-add-a-permission-to-a-user-group-during-a-django-migration
    """
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    view_user = Permission.objects.get(codename="view_user")
    change_user = Permission.objects.get(codename="change_user")

    moderator = Group.objects.get(name=MODERATOR)
    moderator.permissions.add(view_user)
    moderator.permissions.add(change_user)


class Migration(migrations.Migration):
    """django migration"""
    dependencies = []

    operations = [
        migrations.RunPython(create_initial_data),
        migrations.RunPython(add_permissions),
    ]
