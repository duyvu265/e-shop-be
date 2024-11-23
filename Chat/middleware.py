import jwt
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from SiteUser.models import SiteUser
from urllib.parse import parse_qs

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope.get('query_string', b''))
        token = query_string.get(b'token', [None])[0]
        
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = await database_sync_to_async(SiteUser.objects.get)(id=payload['user_id'])
            except jwt.ExpiredSignatureError:
                user = AnonymousUser()
            except jwt.DecodeError:
                user = AnonymousUser()
        else:
            user = AnonymousUser()

        scope['user'] = user
        return await self.inner(scope, receive, send)

from channels.middleware.base import BaseMiddleware

class JWTAuthMiddlewareStack(AuthMiddlewareStack):
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddleware(self.inner)(scope)
