import json
from DoodleChamp_app.models import Lobby, Players
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
def get_players(code):
        lobby_code = code[-4:]
        return list(Players.objects.filter(code = lobby_code))

        #return Players.objects.exclude(name=name).filter(code=code)

class DoodleChamp_appConsumer(AsyncWebsocketConsumer):
    # def __init__(self):
    #     self.username = ""
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
        action_type = text_data_json["type"]
        
        # Send message to room . Puts message on redis
        if action_type == "DoodleChamp_app_player_joins":
            await self.channel_layer.group_send(self.room_group_name, {"type": "set_username", "username": text_data_json["player"]})
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "draw_stroke":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type, "lastX": text_data_json["lastX"],
                                                                        "lastY": text_data_json["lastY"],
                                                                        "currentX": text_data_json["currentX"],
                                                                        "currentY": text_data_json["currentY"],
                                                                        "strokeStyle": text_data_json["strokeStyle"]
            })
        elif action_type == "print_name":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "undo":
            print(text_data_json["pic"])
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type, "pic": text_data_json["pic"]})
        elif action_type == "start_game":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "draw_turn":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "turn_ended":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})

    # Action types
    # Receive message from room group
    
    async def set_username(self, event):
        self.username = event["username"]
        print(self.username)
    
    async def print_name(self, event):
        print("t", self.username)
        
    async def DoodleChamp_app_player_joins(self,event):
        print(self.username)
        users = await sync_to_async(get_players)(code = self.room_group_name) #gets all players in the room except the user to be displayed in the player list
        #print(users)

        await self.send(text_data=json.dumps({"type": "delete_players"}))

        # print("users", users)
        for user in users:
            # print(user.name)
            # name = user.values()["name"]
            await self.send(text_data=json.dumps({"type": "add_players", "player": user.name}))
        
        # Send player info to WebSocket
    
    async def draw_stroke(self, event):
        #print(self.username)
        currentX = event["currentX"]
        currentY = event["currentY"]
        lastX = event["lastX"]
        lastY = event["lastY"]
        #print(currentX, "currentX")
        strokeStyle = event["strokeStyle"]
        
        await self.send(text_data=json.dumps({"type": "draw_stroke",
                                              "currentX": currentX,
                                              "currentY": currentY,
                                              "lastX": lastX, 
                                              "lastY": lastY,
                                              "strokeStyle": strokeStyle}))
        
    # Sends to non-drawers
    async def undo(self, event):
        pic = event["pic"]

        await self.send(text_data=json.dumps({"type": "undo",
                                              "pic": pic}))
    
    async def start_game(self, event):
        await self.send(text_data=json.dumps({"type": "start_game"}))
    
    async def draw_turn(self, event):
        await self.send(text_data=json.dumps({"type": "draw_turn"}))
    async def turn_ended(self, event):
        print("turn_ended")
        await self.send(text_data=json.dumps({"type": "turn_ended"}))
