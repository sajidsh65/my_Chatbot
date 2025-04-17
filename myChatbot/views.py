import os
import requests
from dotenv import load_dotenv
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import ChatHistory, ChatSession
from langchain.memory import ConversationBufferMemory
from django.utils.timezone import now

# Load environment variables
load_dotenv()

# Gemini API key
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY="AIzaSyCNr4imWpCLe1zJspdIzXcYUl9i7KzLlgQ"

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"



# Dictionary to store conversation memory per session
conversation_memories = {}

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_message = data.get("message", "")
            session_id = data.get("session_id")  # Frontend se session_id le rahe hain

            if not user_message:
                return JsonResponse({"error": "Message is required"}, status=400)

            # ✅ **Check if session_id is provided and exists in DB**
            session = None
            if session_id:
                session = ChatSession.objects.filter(session_id=session_id).first()

            # ✅ **Agar session exist nahi karta, sirf tab naya create karo**
            if session is None:
                session_id = str(uuid.uuid4())  # ✅ New ID generate karo
                session = ChatSession.objects.create(
                    session_id=session_id,
                    user=request.user if request.user.is_authenticated else None
                )

           # ✅ **Ensure memory is maintained properly**
            if session_id not in conversation_memories:
                conversation_memories[session_id] = ConversationBufferMemory()

            chat_memory = conversation_memories[session_id]
            
            # if session and not session.is_active:
            #     conversation_memories.pop(session_id, None)
            if session and not session.is_active:
                conversation_memories.pop(session_id, None)
                session_id = str(uuid.uuid4())  # ✅ Generate new ID
                session = ChatSession.objects.create(
                    session_id=session_id,
                    user=request.user
                )
                
            headers = {"Content-Type": "application/json"}
            payload = {"contents": [{"parts": [{"text": user_message}]}]}

            response = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=payload, headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                bot_reply = (
                    result["candidates"][0]["content"]["parts"][0]["text"]
                    if "candidates" in result and result["candidates"]
                    else "No response from Gemini."
                )

                if request.user.is_authenticated:
                    ChatHistory.objects.create(session_id=session, sender="user", message=user_message, timestamp=now())
                    ChatHistory.objects.create(session_id=session, sender="bot", message=bot_reply, timestamp=now())
                
                # ✅ Save chat in LangChain memory
                chat_memory.save_context({"input": user_message}, {"output": bot_reply})

                return JsonResponse({"response": bot_reply, "session_id": session.session_id})

            return JsonResponse({"error": "API request failed", "details": response.text}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=405)


    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_chat_histories(request):
    try:
        user = request.user
        sessions = ChatSession.objects.filter(user=user)
        all_chats = {}

        for session in sessions:
            messages = ChatHistory.objects.filter(session_id=session).order_by("timestamp")
            chat_data = [
                {
                    "sender": msg.sender,
                    "message": msg.message,
                    "timestamp": msg.timestamp,
                }
                for msg in messages
            ]
            # all_chats[session.session_id] = chat_data
            all_chats[str(session.session_id)] = chat_data

        # print(f"📚 All Chat Sessions for {user.username}:", all_chats)
        return Response({"chat_sessions": all_chats}, status=200)

    except Exception as e:
        # print(f"❌ Server Error: {e}")
        import traceback
        traceback.print_exc()  # This will show full error trace in your terminal
        return Response({"error": "Failed to fetch all chat histories."}, status=500)


@api_view(["POST"])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.auth.delete()
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_session(request):
    """New chat session create karne ka endpoint"""
    session_id = str(uuid.uuid4())  # Unique session ID generate karein
    session = ChatSession.objects.create(session_id=session_id, user=request.user)
    return Response({"session_id": session.session_id}, status=201)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_session(request, session_id):
    try:
        session = ChatSession.objects.filter(session_id=session_id, user=request.user).first()
        if not session:
            return Response({"error": "Session not found"}, status=404)

        session.delete()
        return Response({"message": "Session deleted successfully"}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
