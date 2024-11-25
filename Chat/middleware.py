from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from jose import jwt
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        token = None

        for param in scope['query_string'].decode().split('&'):
            if param.startswith('token='):
                token = param.split('=')[1]
                break

        if token is None:
            raise Exception("Token is missing")


        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if user_id is None:
                raise Exception("Invalid token")
            
            user = self.get_user(user_id)
            scope['user'] = user  
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.JWTError:
            raise Exception("Invalid token")

        return self.inner(scope)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")
