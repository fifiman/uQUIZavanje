# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/game/(?P<game_id>[^/]+)/$', consumers.GameConsumer),
    url(r'^ws/user/(?P<user_id>[^/]+)/$', consumers.UserConsumer),

]