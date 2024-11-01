from django.urls import path
from .views import get_chats, send_message, mark_message_as_read

urlpatterns = [
    path('', get_chats, name='get_chats'),
    path('send/', send_message, name='send_message'),
    path('<int:chat_id>/mark-as-read/', mark_message_as_read, name='mark_message_as_read'),
]
