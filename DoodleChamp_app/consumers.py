import json
from DoodleChamp_app.models import Lobby, Players, Words, Game, User, Stats
from DoodleChamp_app.words import word_list, word_dict
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import random
import time
# from django.db.models.functions import Rand

def get_players(code):
    lobby_code = code[-4:]
    names = []
    query = list(Players.objects.filter(code = lobby_code))
    for i in query:
        # print("get_playwers", i.name)
        names.append(i.name)
    return names

def get_players_for_game(code):
    lobby_code = code[-4:]
    names = []
    query = list(Players.objects.filter(code = lobby_code))
    for i in query:
        #print("get_playwers", i.name, i.score)
        names.append([i.name, i.score])
    return names

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
        if curr_id == first_id:
            return True
        else:
            return False
    else:
        #print("test", curr_id)
        curr_player = Players.objects.get(code = lobby_code, isDrawer = True)
        curr_player.isDrawer = False
        curr_player.save()
        next_player = Players.objects.get(code = lobby_code, id = first_id)
        next_player.isDrawer = True
        next_player.save()
        game = Game.objects.get(code = lobby_code)
        game.round = game.round - 1
        game.save()
        return False

def check_round(code):
    lobby_code = code[-4:]
    game = Game.objects.get(code = lobby_code)
    return game.round

def final_scoreboard(code):
    lobby_code = code[-4:]
    scoreboard = []
    scores = list(Players.objects.filter(code=lobby_code).order_by('-score'))
    for i in scores:
        scoreboard.append([i.name, i.score])

    return scoreboard
def calc_stats(code):
    lobby_code = code[-4:]
    first = ""
    top_score = 0
    scores = list(Players.objects.filter(code=lobby_code).order_by('-score'))
    for i in scores:
        if i.score > top_score:
            top_score = i.score
            first = i.name
        
    for i in scores:
        print("scorte", type(i.name))
        if i.name == first:
           winner = Stats.objects.get(user = first) 
           winner.wins = winner.wins + 1
           winner.save()
        else:
            loser = Stats.objects.get(user = i.name) 
            loser.loses = loser.loses + 1
            loser.save()

def get_drawer(code):
    
    lobby_code = code[-4:]
    # l = Players.objects.filter(code = lobby_code, isDrawer = True)
    #print("l", l.values())
    drawer = Players.objects.get(code = lobby_code, isDrawer = True)
    return drawer.name

def set_word(code, word, points):
    lobby_code = code[-4:]
    word_ = Game.objects.get(code = lobby_code)
    word_.active_word = word
    word_.point_value = points
    word_.save()

def set_num_rounds(code, n):
    lobby_code = code[-4:]
    round_ = Game.objects.get(code = lobby_code)
    round_.round = n
    round_.save()
    print('num rounds: ', round_.round)

def curr_word(code):
    lobby_code = code[-4:]
    word = Game.objects.get(code = lobby_code)
    return word

def delete_lobby(code):
    lobby_code = code[-4:]
    exists = Lobby.objects.filter(code = lobby_code)
    if len(exists.values()) == 1:
        Lobby.objects.get(code = lobby_code).delete()

def add_words():
    if not Words.objects.exists(): 
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
def calc_points(code, player, points):

    lobby_code = code[-4:]
    user = User.objects.get(username = player)
    print("c", user)
    score = Players.objects.get(code = lobby_code, name = user)
    print("score", score)
    score.score = score.score + points
    print(score.score)
    score.save()


def get_words():
    # count = Words.objects.count()
    # random_index = random.randint(0, count - 1)
    # random_obj = Words.objects.all()[random_index]
    # return list(random_obj)
    # add_words()
    words = Words.objects.all()
    return list(words)



class DoodleChamp_appConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_round = 0
    
        
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
        elif action_type == "draw_rect":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type, "lastX": text_data_json["lastX"],
                                                                        "lastY": text_data_json["lastY"],
                                                                        "currentX": text_data_json["currentX"],
                                                                        "currentY": text_data_json["currentY"],
                                                                        "strokeStyle": text_data_json["strokeStyle"]
        })
        elif action_type == "draw_line":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type, "lastX": text_data_json["lastX"],
                                                                        "lastY": text_data_json["lastY"],
                                                                        "currentX": text_data_json["currentX"],
                                                                        "currentY": text_data_json["currentY"],
                                                                        "strokeStyle": text_data_json["strokeStyle"]
        })
        elif action_type == "draw_circle":
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
        elif action_type == "show_round_settings":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type, "round_setting": text_data_json["round_setting"]})
            
        elif action_type == "next_player":
            
            print("next player")
            
            round = await sync_to_async(check_round)(code = self.room_group_name)
            print(round)
            if round <= 0:
                await self.channel_layer.group_send(self.room_group_name, {"type": "end_game"})
                await sync_to_async(calc_stats)(code = self.room_group_name)
                
            else:
                
                change_round = await sync_to_async(player_rotate)(code = self.room_group_name)
                if change_round == True:
                    await self.channel_layer.group_send(self.room_group_name, {"type": "next_round"})
                    
        elif action_type == "turn_ended":
             #is here since it only needs to be executed once
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "delete_lobby":
            await sync_to_async(delete_lobby)(code = self.room_group_name)
        elif action_type == "empty_chat":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "set_player_list":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "set_word":
            await sync_to_async(set_word)(code = self.room_group_name, word = text_data_json["word"], points = text_data_json["points"])
            await self.channel_layer.group_send(self.room_group_name, {"type": "show_word"})
        
        elif action_type == "set_num_rounds":
            await sync_to_async(set_num_rounds)(code = self.room_group_name, n = text_data_json["num_rounds"])
            # await self.channel_layer.group_send(self.room_group_name, {"type":  action_type})
            
            # await self.channel_layer.group_send(self.room_group_name, {"type": "round"})
        elif action_type == "guess":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type, "guess": text_data_json["guess"], "player": text_data_json["player"]})
    # Action types
    # Receive message from room group
    
    async def set_username(self, event):
        self.username = event["username"]
        print("1", self.username)
    
    async def print_name(self, event):
        print("t", self.username)
        
    async def DoodleChamp_app_player_joins(self,event):
        #print("add")
        users = await sync_to_async(get_players)(code = self.room_group_name) #gets all players in the room except the user to be displayed in the player list
        #print(users)

        await self.send(text_data=json.dumps({"type": "delete_players"}))

        # print("users", users)
        for user in users:
            # print("2:", user)
            name = str(user)#needs to be converted to a string
            # print("name", str(name))
            await self.send(text_data=json.dumps({"type": "add_players", "player": name}))
            # await self.send(text_data=json.dumps({"type": "add_players", "player": f"{user.name} | {user.score}"}))

        
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
    async def draw_rect(self, event):
        #print(self.username)
        currentX = event["currentX"]
        currentY = event["currentY"]
        lastX = event["lastX"]
        lastY = event["lastY"]
        #print(currentX, "currentX")
        strokeStyle = event["strokeStyle"]
        
        await self.send(text_data=json.dumps({"type": "draw_rect",
                                              "currentX": currentX,
                                              "currentY": currentY,
                                              "lastX": lastX, 
                                              "lastY": lastY,
                                              "strokeStyle": strokeStyle}))

    async def draw_line(self, event):
        #print(self.username)
        currentX = event["currentX"]
        currentY = event["currentY"]
        lastX = event["lastX"]
        lastY = event["lastY"]
        #print(currentX, "currentX")
        strokeStyle = event["strokeStyle"]
        await self.send(text_data=json.dumps({"type": "draw_line",
                                              "currentX": currentX,
                                              "currentY": currentY,
                                              "lastX": lastX, 
                                              "lastY": lastY,
                                              "strokeStyle": strokeStyle}))

    async def draw_circle(self, event):
        #print(self.username)
        currentX = event["currentX"]
        currentY = event["currentY"]
        lastX = event["lastX"]
        lastY = event["lastY"]
        #print(currentX, "currentX")
        strokeStyle = event["strokeStyle"]
        await self.send(text_data=json.dumps({"type": "draw_circle",
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

    async def show_round_settings(self, event):
        n_rounds = event["round_setting"]
        # print('n_rounds: ', type(n_rounds))
        await self.send(text_data=json.dumps({"type": "show_round_settings", "num_rounds": n_rounds}))
    
    async def start_game(self, event):
        await sync_to_async(add_words)()
        await self.send(text_data=json.dumps({"type": "start_game"}))
    
    async def see_words(self, event):
        # await self.send(text_data=json.dumps({"type": "see_words"}))
        words = await sync_to_async(get_words)()
        # print(words, "words")

        word1 = random.choice(words)
        word2 = random.choice(words)

        await self.send(text_data=json.dumps({"type": "see_words", "word1": word1.word, "value1": word1.point_value, "word2": word2.word, "value2": word2.point_value}))

    async def draw_turn(self, event):
        # Note: Update scores here with a function
        print("new_turn")
        drawer = await sync_to_async(get_drawer)(code = self.room_group_name)
        users = await sync_to_async(get_players_for_game)(code = self.room_group_name)

        print("drawer", drawer)
        #delete players
        #show scores
        await self.send(text_data=json.dumps({"type": "delete_players"}))
        for user in users:
            print("dturn", str(user[1]))
            await self.send(text_data=json.dumps({"type": "add_players", "player": f"{str(user[0])} | {str(user[1])}"}))
        await self.send(text_data=json.dumps({"type": "show_drawer", "player": str(drawer)}))
        await self.send(text_data=json.dumps({"type": "draw_turn", "player": str(drawer)}))
        


    async def turn_ended(self, event):
        # await sync_to_async(player_rotate)(code = self.room_group_name)
        # users = await sync_to_async(get_players)(code = self.room_group_name) #gets all players in the room except the user to be displayed in the player list
        await self.send(text_data=json.dumps({"type": "turn_ended"}))
        # await self.send(text_data=json.dumps({"type": "delete_players"}))
        # for user in users:
        #     await self.send(text_data=json.dumps({"type": "add_players", "player": f"{user.name} | {user.score}"}))
        
        print("turn ended")

    async def empty_chat(self, event):
        await self.send(text_data=json.dumps({"type": "empty_chat"}))      

    async def show_word(self, event):
        current_word = await sync_to_async(curr_word)(code = self.room_group_name)
        
        new_string = " ".join("_" * len(c) for c in current_word.active_word)
        print(current_word.active_word, new_string)
        # await self.send(text_data=json.dumps({"type": "hidden_word", "word": new_string}))
        await self.send(text_data=json.dumps({"type": "hidden_word", "word": new_string, "actual_word": current_word.active_word}))

        self.guess_list = []

    async def guess(self, event):
        current_word = await sync_to_async(curr_word)(code = self.room_group_name)
        guess = event["guess"]
        player = event["player"]
        if guess == current_word.active_word:
            await self.send(text_data=json.dumps({"type": "guess_return", "msg": f"{player} has guessed the word: {guess}"}))
            await self.channel_layer.group_send(self.room_group_name, {"type": "round", "player": player})
        else:
            await self.send(text_data=json.dumps({"type": "guess_return", "msg": f"{player}: {guess}"}))


    async def round(self, event):
        print("round")
        num_players = await sync_to_async(get_players)(code = self.room_group_name)
        current_word = await sync_to_async(curr_word)(code = self.room_group_name)
        points = current_word.point_value
        num_players = len(num_players)
        self.guess_list.append(event["player"])
        if len(self.guess_list) == num_players - 1:
            #compute score
            for i, user in enumerate(self.guess_list):
                calced_points = ((num_players - i)/num_players) * points
                print("test:", user)
                await sync_to_async(calc_points)(code = self.room_group_name, player = user, points = calced_points)
            print("done calculating points")
            self.guess_list = []
            print(self.guess_list)
            await self.channel_layer.group_send(self.room_group_name, {"type": "turn_ended"})
            await self.channel_layer.group_send(self.room_group_name, {"type": "draw_turn"})

    async def end_game(self, event):
        scoreboard = await sync_to_async(final_scoreboard)(code = self.room_group_name)
        print(scoreboard)
        for i, user in enumerate(scoreboard):
            print("endgame", i)
            await self.send(text_data=json.dumps({"type": "end_game", "prompt": f"{i + 1}: {user[0]} Points: {user[1]}"}))
        await self.send(text_data=json.dumps({"type": "end_modal"}))
        
    
    async def next_round(self, event):
        self.num_round += 1
        await self.send(text_data=json.dumps({"type": "next_round", "round": self.num_round}))
        

        
        
    # async def game(self, event):
    #     #first player in self.player_rotation should be selected and given permission to draw
    #     drawer = self.player_rotation[0]
        
        