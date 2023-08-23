from django.apps import AppConfig

class FileDescriptorConfig(AppConfig):
    default_auto_filed = 'django.db.models.BigAutoField'
    name = 'cubeseed.filedescriptor'