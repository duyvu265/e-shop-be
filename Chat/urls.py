from django.urls import path
from . import views

urlpatterns = [
    path('api/chat-sessions/', views.chat_sessions, name='chat_sessions'),
    path('api/chat-sessions/<int:chat_session_id>/messages/', views.messages, name='messages'),
    path('api/messages/<int:message_id>/mark-as-read/', views.mark_message_as_read, name='mark_message_as_read'),
    path('api/chat-sessions/<int:chat_session_id>/typing/', views.typing_status, name='typing_status'),
    path('api/chat-sessions/<int:chat_session_id>/stop-typing/', views.stop_typing, name='stop_typing'),
    path('api/notifications/', views.notifications, name='notifications'),
    path('api/notifications/<int:notification_id>/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
]
