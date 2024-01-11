from .settings_prod import *

ALLOWED_HOSTS = ["localhost"]

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "TEST": {
            "NAME": BASE_DIR / "test_db.sqlite3",
        },
    }
}

REST_FRAMEWORK["TEST_REQUEST_DEFAULT_FORMAT"] = "json"
REST_FRAMEWORK["TEST_REQUEST_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.MultiPartRenderer", # To handle file uploads(for multipart format support) when testing
]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Setup channel layers
CHANNEL_LAYERS = {
    'default': {
        # For development
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
        # For production
        # Use redis
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     'hosts': [(env('REDIS_HOST'), env.int('REDIS_PORT'))],
        # },
    }
}
