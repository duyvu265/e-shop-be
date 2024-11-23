import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import ChatSession, Message, TypingStatus


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope.get('query_string', b'').decode().split('=')[-1]  

        try:
            access_token = AccessToken(token)
            user = await database_sync_to_async(get_user_model().objects.get)(id=access_token['user_id'])

            self.scope['user'] = user 
        except Exception as e:
            print(f"Token validation failed: {e}")
            await self.close()  
            return

        self.chat_session_id = self.scope['url_route']['kwargs']['chat_session_id']
        self.chat_session = await database_sync_to_async(ChatSession.objects.get)(id=self.chat_session_id)

        if self.scope['user'] != self.chat_session.customer and not self.scope['user'].is_staff:
            await self.close() 
            return

        self.room_group_name = f"chat_{self.chat_session_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.send(text_data=json.dumps({
            'message': f'User {self.scope["user"].email} has entered the chat.'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']  

        chat_session = await database_sync_to_async(ChatSession.objects.get)(id=self.chat_session_id)
        new_message = await database_sync_to_async(Message.objects.create)(
            chat_session=chat_session,
            sender=sender,
            message=message,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': new_message.message,
                'sender': sender.email,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    async def typing_status(self, event):
        is_typing = event['is_typing']
        user = event['user']

        await self.send(text_data=json.dumps({
            'typing_status': is_typing,
            'user': user,
        }))

    async def receive_typing_status(self, text_data):
        data = json.loads(text_data)
        if data.get('is_typing') is not None:
            user = self.scope['user']
            is_typing = data['is_typing']
            chat_session = await database_sync_to_async(ChatSession.objects.get)(id=self.chat_session_id)

            await database_sync_to_async(TypingStatus.objects.update_or_create)(
                user=user, chat_session=chat_session, defaults={'is_typing': is_typing}
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_status',
                    'is_typing': is_typing,
                    'user': user.email,
                }
            )
