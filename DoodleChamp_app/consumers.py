import json
from DoodleChamp_app.models import Lobby
from channels.generic.websocket import AsyncWebsocketConsumer

class DoodleChamp_appConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "DoodleChamp_app%s" % self.room_name
        print("right here", self.room_group_name)

        # Join room group
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from a client browser over a WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        player = text_data_json["player"]

        # Send message to room . Puts message on redis
        await self.channel_layer.group_send(self.room_group_name, {"type": "DoodleChamp_app_player_joins", "player": player})

    # Receive message from room group
    async def DoodleChamp_app_player_joins(self,event):
        player = event["player"]

        # Send player info to WebSocket
        await self.send(text_data=json.dumps({"player": player}))