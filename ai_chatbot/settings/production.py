# ai_chatbot/settings/production.py

from .base import *
import dj_database_url

DEBUG = False
# ALLOWED_HOSTS = ["your-backend.onrailway.app", "localhost"]
ALLOWED_HOSTS = [
    "https://chatbot-bysajid-3685.up.railway.app/",
    "https://chatbot-bysajid.vercel.app"
]


DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("DB_NAME"),
#         "USER": os.getenv("DB_USER"),
#         "PASSWORD": os.getenv("DB_PASSWORD"),
#         "HOST": os.getenv("DB_HOST"),
#         "PORT": os.getenv("DB_PORT", "5432"),
#     }
# }
