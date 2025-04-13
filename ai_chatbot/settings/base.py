# ai_chatbot/settings/base.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
DJANGO_SECRET_KEY="#kxvkw4up#d393kco&&ii0)()u2&6nohx=v8h0l&z1=y@#b^@g"
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-secret-key")
DEBUG = False

ALLOWED_HOSTS = []
ALLOWED_HOSTS = [
    "chatbot-bysajid-3685.up.railway.app",
    "https://chatbot-bysajid.vercel.app",
    "localhost",  # Optional, for local development
    "127.0.0.1",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "myChatbot",
    "corsheaders",
]

MIDDLEWARE = [
    
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
]

ROOT_URLCONF = "ai_chatbot.urls"

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

WSGI_APPLICATION = "ai_chatbot.wsgi.application"

# Auth
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True
# Allow local frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://chatbot-bysajid.vercel.app/",
    "https://chatbot-bysajid-3685.up.railway.app",  # optional
]


CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "conversation-id",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "django_error.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
