import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token = None
        if 'token' in scope['query_string']:
            token = scope['query_string'].decode().split('=')[1]
        if token:
            try:
                access_token = AccessToken(token)
                user = await self.get_user_from_token(access_token)
                scope['user'] = user
            except Exception as e:
                print("Token invalid:", e)
                scope['user'] = AnonymousUser() 
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, access_token):
        try:
            user_id = access_token['user_id']
            user = get_user_model().objects.get(id=user_id)
            return user
        except get_user_model().DoesNotExist:
            return None
