from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ChatSession, Message, TypingStatus, Notification
from .serializer import ChatSessionSerializer, MessageSerializer, NotificationSerializer
from SiteUser.models import SiteUser

@api_view(['GET', 'POST'])
def chat_sessions(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        user = request.user.siteuser
        chat_sessions = ChatSession.objects.filter(participants=user)
        serializer = ChatSessionSerializer(chat_sessions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChatSessionSerializer(data=request.data)
        if serializer.is_valid():
            chat_session = serializer.save()
            chat_session.participants.add(request.user.siteuser)
            admin_user = SiteUser.objects.filter(user_type='admin').first()
            if admin_user:
                chat_session.participants.add(admin_user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def messages(request, chat_session_id):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        chat_session = ChatSession.objects.get(id=chat_session_id)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Chat session not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        messages = Message.objects.filter(chat_session=chat_session)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        sender = request.user.siteuser
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat_session=chat_session, sender=sender)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mark_message_as_read(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return Response({'status': 'message marked as read'})
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def typing_status(request, chat_session_id):
    try:
        chat_session = ChatSession.objects.get(id=chat_session_id)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Chat session not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user.siteuser
    typing_status, created = TypingStatus.objects.get_or_create(
        user=user, chat_session=chat_session, defaults={'is_typing': True}
    )
    if not created:
        typing_status.is_typing = True
        typing_status.save()

    return Response({'status': 'typing'})

@api_view(['POST'])
def stop_typing(request, chat_session_id):
    try:
        chat_session = ChatSession.objects.get(id=chat_session_id)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Chat session not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user.siteuser
    try:
        typing_status = TypingStatus.objects.get(user=user, chat_session=chat_session)
        typing_status.is_typing = False
        typing_status.save()
        return Response({'status': 'stopped typing'})
    except TypingStatus.DoesNotExist:
        return Response({'error': 'Typing status not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def notifications(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        notifications = Notification.objects.filter(user=request.user.siteuser)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        message_id = request.data.get('message_id')
        try:
            message = Message.objects.get(id=message_id)
            serializer = NotificationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user.siteuser, message=message)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
