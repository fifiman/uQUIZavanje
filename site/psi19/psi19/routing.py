from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

import quiz.consumers

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)

    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/game/<int:game_id>',       quiz.consumers.GameConsumer)
        ]
        )
    ),
})