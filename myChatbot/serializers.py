from rest_framework import serializers
from .models import ChatSession, ChatHistory

# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields = '__all__'

class ChatSessionSerializer(serializers.ModelSerializer):
    # messages = MessageSerializer(many=True, read_only=True)  # Include messages in session
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    
    class Meta:
        model = ChatSession
        fields = '__all__'
        
class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = "__all__"