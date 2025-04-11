

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    register_user, login_user,get_all_chat_histories, logout_user, chatbot_response, create_session)

urlpatterns = [
    path('api/register/', register_user, name='register'),
    path('api/login/', login_user, name='login'),
    path('api/logout/', logout_user, name='logout'),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/chat/', chatbot_response, name='chatbot_response'),
    path("api/create-session/", create_session, name="create_session"),
    path("api/all-chat-histories/", get_all_chat_histories, name="all-chat-histories"),

]

