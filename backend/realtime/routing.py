from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Matches the contract: wss://api.cricketops.example/ws/matches/{public_match_id}
    re_path(r'ws/matches/(?P<match_id>[\w-]+)/?$', consumers.MatchConsumer.as_asgi()),
]