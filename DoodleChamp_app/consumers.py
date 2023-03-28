import json
from DoodleChamp_app.models import Lobby, Players
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
def get_players(code):
        lobby_code = code[-4:]
        return list(Players.objects.filter(code = lobby_code))

        #return Players.objects.exclude(name=name).filter(code=code)

class DoodleChamp_appConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "DoodleChamp_app%s" % self.room_name
        

        print("right here", self.room_group_name)

        # Join room group
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #self.channel_layer.channel_layer[self.channel_name]["username"] = username

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from a client browser over a WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.username = text_data_json["player"]
        print("self.username",self.username)

        # Send message to room . Puts message on redis
        await self.channel_layer.group_send(self.room_group_name, {"type": "DoodleChamp_app_player_joins", "player": self.username})

    # Receive message from room group
    def get_players(self, name, code):
        return Players.objects.exclude(name=name).filter(code=code)
        
    async def DoodleChamp_app_player_joins(self,event):
        
        users = await sync_to_async(get_players)(code = self.room_group_name) #gets all players in the room except the user to be displayed in the player list
        #print(users)

        # print("users", users)
        for user in users:
            print(user.name)
            # name = user.values()["name"]
            await self.send(text_data=json.dumps({"player": user.name}))
        
        # Send player info to WebSocket

        