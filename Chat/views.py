from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatSession, Message, TypingStatus
from .serializer import ChatSessionSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chat_session_list(request):
    if request.method == 'GET':
        chats = ChatSession.objects.filter(participants=request.user.siteuser)
        serializer = ChatSessionSerializer(chats, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChatSessionSerializer(data=request.data)
        if serializer.is_valid():
            chat_session = serializer.save()
            chat_session.participants.add(request.user.siteuser)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def message_list_create(request, chat_session_id):
    chat_session = get_object_or_404(ChatSession, id=chat_session_id)

    if request.method == 'GET':
        messages = Message.objects.filter(chat_session=chat_session)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['chat_session'] = chat_session.id
        data['sender'] = request.user.siteuser.id
        serializer = MessageSerializer(data=data)
        
        if serializer.is_valid():
            message = serializer.save()
            message.status = 'sent'
            message.save()
            TypingStatus.objects.filter(user=request.user.siteuser, chat_session=chat_session).delete()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def chat_session_detail(request, pk):
    chat_session = get_object_or_404(ChatSession, pk=pk)

    if request.method == 'GET':
        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ChatSessionSerializer(chat_session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        chat_session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def typing_status(request, chat_session_id):
    chat_session = get_object_or_404(ChatSession, id=chat_session_id)
    is_typing = request.data.get('is_typing', False)
    typing_status, created = TypingStatus.objects.get_or_create(
        user=request.user.siteuser,
        chat_session=chat_session
    )

    typing_status.is_typing = is_typing
    typing_status.save()

    return Response({'status': 'success'}, status=status.HTTP_200_OK)
