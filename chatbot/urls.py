from django.urls import path
from chatbot import views
from .views import openai_chat

urlpatterns = [
    path('openai-chat/', openai_chat, name='openai_chat'),
    path('', views.render_history_chat, name='history_chat'),
]
