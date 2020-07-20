from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from peps.consumers import MessageConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r'ws/messages/(?P<farmer_id>[0-9a-f-]+)/?$', MessageConsumer),
            ]
        )
    ),
})
