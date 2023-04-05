import json
from DoodleChamp_app.models import Lobby, Players, Words, Game
from DoodleChamp_app.words import word_list, word_dict
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import random
# from django.db.models.functions import Rand

def get_players(code):
    lobby_code = code[-4:]
    return list(Players.objects.filter(code = lobby_code))

    # return Players.objects.exclude(name=name).filter(code=code)

def player_rotate(code):
    lobby_code = code[-4:]
    players = list(Players.objects.filter(code = lobby_code))
    current_drawer = list(Players.objects.filter(code = lobby_code, isDrawer = True))
    #print("rotate")
    curr_id = current_drawer[0].id
    first_id = players[0].id
    max_id = players[len(players) - 1].id
    if curr_id != max_id:
        curr_player = Players.objects.get(code = lobby_code, isDrawer = True)
        curr_player.isDrawer = False
        curr_player.save()
        next_player = Players.objects.get(code = lobby_code, id = curr_id + 1)
        next_player.isDrawer = True
        next_player.save()
    else:
        #print("test", curr_id)
        curr_player = Players.objects.get(code = lobby_code, isDrawer = True)
        curr_player.isDrawer = False
        curr_player.save()
        next_player = Players.objects.get(code = lobby_code, id = first_id)
        next_player.isDrawer = True
        next_player.save()

def get_drawer(code):
    
    lobby_code = code[-4:]
    # l = Players.objects.filter(code = lobby_code, isDrawer = True)
    #print("l", l.values())

    return list(Players.objects.filter(code = lobby_code, isDrawer = True))

def set_word(code, word):
    lobby_code = code[-4:]
    word = Game.objects.get(code = lobby_code)
    word.active_word = word
    word.save()
def curr_word(code):
    lobby_code = code[-4:]
    word = Game.objects.get(code = lobby_code)
    return word.active_word
def add_words():
    words_count = Words.objects.all()
    # print(words_count.count())
    if words_count.count() == 0: 
        for i in word_list:
            length = len(i)
            if length <= 4:
                word_dict[i] = 50
            elif length <= 7:
                word_dict[i] = 100
            elif length <= 11:
                word_dict[i] = 150
            elif length > 11:
                word_dict[i] = 200

        for i in word_list:
            Words.objects.create(word = i, point_value = word_dict[i])
        print("added")
    else:
        print("passed")
        pass


def get_words():
    # count = Words.objects.count()
    # random_index = random.randint(0, count - 1)
    # random_obj = Words.objects.all()[random_index]
    # return list(random_obj)
    # add_words()
    words = Words.objects.all()
    return list(words)

class DoodleChamp_appConsumer(AsyncWebsocketConsumer):
    # def __init__(self):
    #     self.username = ""
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "DoodleChamp_app%s" % self.room_name
        

        #print("right here", self.room_group_name)

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
            #print(text_data_json["pic"])
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type, "pic": text_data_json["pic"]})
        elif action_type == "start_game":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "see_words":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "draw_turn":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "turn_ended":
            await sync_to_async(player_rotate)(code = self.room_group_name) #is here since it only needs to be executed once
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "set_player_list":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})

    # Action types
    # Receive message from room group
    
    async def set_username(self, event):
        self.username = event["username"]
        print(self.username)
    
    async def print_name(self, event):
        print("t", self.username)
        
    async def DoodleChamp_app_player_joins(self,event):
        #print("add")
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
        await sync_to_async(add_words)()
        await self.send(text_data=json.dumps({"type": "start_game"}))
    
    async def see_words(self, event):
        # await self.send(text_data=json.dumps({"type": "see_words"}))
        words = await sync_to_async(get_words)()
        print(words, "words")

        word1 = random.choice(words)
        word2 = random.choice(words)

        await self.send(text_data=json.dumps({"type": "see_words", "word1": word1.word, "value1": word1.point_value, "word2": word2.word, "value2": word2.point_value}))

    async def draw_turn(self, event):
        drawer = await sync_to_async(get_drawer)(code = self.room_group_name)
        #print("drawer", drawer)
        await self.send(text_data=json.dumps({"type": "show_drawer", "player": drawer[0].name}))
        await self.send(text_data=json.dumps({"type": "draw_turn", "player": drawer[0].name}))
        


    async def turn_ended(self, event):
        # await sync_to_async(player_rotate)(code = self.room_group_name)
        await self.send(text_data=json.dumps({"type": "turn_ended"}))

    
    async def round(self, event):
        pass
    # async def game(self, event):
    #     #first player in self.player_rotation should be selected and given permission to draw
    #     drawer = self.player_rotation[0]
        
        