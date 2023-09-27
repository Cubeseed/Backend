from .settings_prod import *

ALLOWED_HOSTS = ["localhost"]

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

REST_FRAMEWORK["TEST_REQUEST_DEFAULT_FORMAT"] = "json"
REST_FRAMEWORK["TEST_REQUEST_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.MultiPartRenderer", # To handle file uploads(for multipart format support) when testing
]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
