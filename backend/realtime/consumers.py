import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the match public ID from the URL route
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.match_group_name = f'match_{self.match_id}'

        # Join the Redis match group
        await self.channel_layer.group_add(
            self.match_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the match group on disconnect
        await self.channel_layer.group_discard(
            self.match_group_name,
            self.channel_name
        )

    # Receive events dispatched from the Django scoring engine
    async def match_event(self, event):
        payload = event['payload']
        
        # Broadcast the event payload to the connected WebSocket client
        await self.send(text_data=json.dumps(payload))