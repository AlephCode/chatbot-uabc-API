from django.urls import path
from chatbot import views
from .views import openai_chat, chat_history

urlpatterns = [
    path('openai-chat/', openai_chat, name='openai_chat'),
    path('chat-history/', chat_history, name='chat_history'),
]
