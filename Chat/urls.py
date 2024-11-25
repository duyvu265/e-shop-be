from django.urls import path
from . import views

urlpatterns = [
    path('chat-sessions/', views.chat_sessions, name='chat_sessions'),
    path('chat-sessions/<int:chat_session_id>/messages/', views.messages, name='messages'),
    path('messages/<int:message_id>/mark-as-read/', views.mark_message_as_read, name='mark_message_as_read'),
    path('chat-sessions/<int:chat_session_id>/typing/', views.typing_status, name='typing_status'),
    path('chat-sessions/<int:chat_session_id>/stop-typing/', views.stop_typing, name='stop_typing'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
]
