"""
This module defines a Celery application instance for the Cubeseed project
named "app" to handle asynchronous tasks in the project.

The Celery application instance is configured using the settings
defined in the Django project's settings module.
"""

from celery import Celery
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cubeseed.settings")

# Create a Celery application instance for the Cubeseed project.
app = Celery("cubeseed")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
