from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/matches/(?P<match_id>[0-9a-fA-F-]+)/?$', consumers.MatchConsumer.as_asgi()),
]