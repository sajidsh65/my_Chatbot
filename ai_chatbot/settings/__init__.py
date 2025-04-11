# ai_chatbot/settings/__init__.py

import os

# Default to local settings if not specified
ENV = os.getenv("DJANGO_ENV", "local")

if ENV == "production":
    from .production import *
else:
    from .local import *
