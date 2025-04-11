from django.contrib import admin
from .models import ChatSession, ChatHistory

admin.site.register(ChatSession)
admin.site.register(ChatHistory)