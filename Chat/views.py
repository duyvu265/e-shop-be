from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializer import ChatSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chats(request):
    user = request.user
   
    chats = Chat.objects.filter(customer=user) | Chat.objects.filter(seller=user)
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    serializer = ChatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_message_as_read(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
        chat.is_read = True
        chat.save()
        return Response({'message': 'Message marked as read'}, status=status.HTTP_200_OK)
    except Chat.DoesNotExist:
        return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
