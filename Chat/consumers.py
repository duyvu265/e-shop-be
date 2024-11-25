import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatSession, Message, TypingStatus
from channels.db import database_sync_to_async
from SiteUser.models import SiteUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_session_id = self.scope['url_route']['kwargs']['chat_session_id']
        self.chat_session = await self.get_chat_session()

        if self.scope['user'] not in [self.chat_session.user, self.chat_session.admin]:
            await self.close()
            return

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
        user_id = text_data_json['user_id']
        is_typing = text_data_json.get('is_typing', None)

        chat_session = await self.get_chat_session()
        sender = await self.get_user(user_id)
        new_message = Message.objects.create(
            chat_session=chat_session,
            sender=sender,
            message=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': new_message.message,
                'sender': sender.user.email
            }
        )

        if is_typing is not None:
            await self.set_typing_status(is_typing, sender)

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def typing_status(self, event):
        is_typing = event['is_typing']
        user = event['user']

        await self.send(text_data=json.dumps({
            'is_typing': is_typing,
            'user': user
        }))

    async def get_chat_session(self):
        return await database_sync_to_async(ChatSession.objects.get)(id=self.chat_session_id)

    async def get_user(self, user_id):
        return await database_sync_to_async(SiteUser.objects.get)(id=user_id)

    async def set_typing_status(self, is_typing, user):
        typing_status, created = TypingStatus.objects.get_or_create(
            user=user,
            chat_session=self.chat_session
        )
        typing_status.is_typing = is_typing
        typing_status.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_status',
                'is_typing': is_typing,
                'user': user.user.email
            }
        )
