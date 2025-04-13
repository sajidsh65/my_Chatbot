# ai_chatbot/settings/local.py

from .base import *
import dj_database_url

DEBUG = True
ALLOWED_HOSTS = [
    "chatbot-bysajid-3685.up.railway.app",
    "https://chatbot-bysajid.vercel.app",
    # "localhost",  # Optional, for local development
    # "127.0.0.1",
]

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("DB_NAME", "mychatdb"),
#         "USER": os.getenv("DB_USER", "postgres"),
#         "PASSWORD": os.getenv("DB_PASSWORD", "sajid6576"),
#         "HOST": os.getenv("DB_HOST", "localhost"),
#         "PORT": os.getenv("DB_PORT", "5432"),
#     }
# }
