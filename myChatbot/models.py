
from django.db import models
from django.contrib.auth.models import User
import uuid

class ChatSession(models.Model):
    """
    This model stores the chat session information.
    Each user can have multiple chat sessions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique Session ID
    created_at = models.DateTimeField(auto_now_add=True)  # Session start time
    is_active = models.BooleanField(default=True)  # Track active/inactive sessions

    def __str__(self):
        return f"Session {self.session_id} - {self.user.username}"


class ChatHistory(models.Model):
    """
    This model stores individual chat messages.
    Each message belongs to a specific chat session.
    """
    session_id = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages", db_column="session_id")  
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("bot", "Bot")], default="user")  
    message = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Session {self.session_id.session_id} - {self.sender}: {self.message[:50]}"
