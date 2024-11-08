import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatSession, Message, TypingStatus
from .serializer import MessageSerializer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_session_id = self.scope['url_route']['kwargs']['chat_session_id']
        self.chat_session = await sync_to_async(ChatSession.objects.get)(id=self.chat_session_id)

        self.room_group_name = f"chat_{self.chat_session.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        status = text_data_json.get('status', 'sent')

        message_obj = await sync_to_async(Message.objects.create)(
            chat_session=self.chat_session,
            sender_id=sender_id,
            message=message,
            status=status
        )

        message_data = MessageSerializer(message_obj).data
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data,
            }
        )

    async def receive_typing(self, text_data):
        text_data_json = json.loads(text_data)
        user_id = text_data_json['user_id']
        is_typing = text_data_json['is_typing']

        typing_status = await sync_to_async(TypingStatus.objects.update_or_create)(
            user_id=user_id,
            chat_session=self.chat_session,
            defaults={'is_typing': is_typing}
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_status',
                'user_id': user_id,
                'is_typing': is_typing
            }
        )
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def typing_status(self, event):
        user_id = event['user_id']
        is_typing = event['is_typing']
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'is_typing': is_typing,
        }))
