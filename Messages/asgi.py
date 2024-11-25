import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import ChatConsumer
from .middleware import JWTAuthMiddleware
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_shop_project.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter([
            path('ws/chat/<int:chat_id>/', ChatConsumer.as_asgi()),
        ])
    ),
})
