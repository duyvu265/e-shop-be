from django.urls import path
from .views import chat_session_list, message_list_create, chat_session_detail

urlpatterns = [
    path('', chat_session_list, name='chat_session_list'),
    path('<int:pk>/', chat_session_detail, name='chat_session_detail'),
    path('<int:chat_session_id>/messages/', message_list_create, name='message_list_create'),
]
