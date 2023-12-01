# import django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import environ

env = environ.Env()
env.read_env()


def run():
    User = get_user_model()

    if not User.objects.filter(username="testuser_1").exists():
        user = User.objects.create_user(username="testuser_1", password=env.str("USER1PASSWORD", ""))
        user.is_active = True
        user.groups.add(Group.objects.get(name="farmer"))
        user.save()
    if not User.objects.filter(username="testuser_2").exists():
        user = User.objects.create_user(username="testuser_2", password=env.str("USER2PASSWORD", ""))
        user.is_active = True
        user.groups.add(Group.objects.get(name="farmer"))
        user.save()