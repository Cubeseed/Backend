from pathlib import Path
import os
import subprocess
from pathlib import Path
import subprocess
import environ

env = environ.Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-iwai)rfl5ls2r=+i_37yl08zuf77qwmbexdx^q_g_r+ovgei-e"
SECRET_KEY = os.getenv("SECRET_KEY", SECRET_KEY)

ALLOWED_HOSTS = ["ec2-16-171-43-115.eu-north-1.compute.amazonaws.com"]

CORS_ORIGIN_ALLOW_ALL = True

DEBUG = False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "cubeseed.userauth",
    "cubeseed.userprofile",
    "cubeseed.filedescriptor",
    "cubeseed.address",
    "cubeseed.businessprofile",
    "cubeseed.farm",
    "cubeseed.commodity",
    "cubeseed.cluster",
    "cubeseed.course",
    "cubeseed.course_verification",
    "cubeseed.purchase_orders",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cubeseed.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cubeseed.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# FIXME: this is a simplification for the MVP, should be using cloud storage.
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"], cwd=BASE_DIR).decode("utf-8").strip()

# Simplify address lookup by restricting to given countries
COUNTRY_CODES = ["NG"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'cubeseedapi'), 
        'USER': os.getenv('DB_USER', 'cubeseed'),
        'PASSWORD': os.getenv('DB_PASS', 'cubeseedsecret'),
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}

# S3 BUCKET CONFIGURATION

# Set USE_S3 to True in the .env file if 
# you want to use AWS S3 for storing media files (Production)
# Otherwise, media files will be stored locally (Development)
USE_S3 = env.bool("USE_S3", False)
if USE_S3:
    # AWS S3 CONFIGURATION
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
    AWS_S3_SIGNATURE_VERSION = env("AWS_S3_SIGNATURE_NAME")
    DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE")
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"
