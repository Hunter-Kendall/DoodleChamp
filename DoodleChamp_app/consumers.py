import json
from DoodleChamp_app.models import Lobby, Players, Words
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import random
def get_players(code):
        lobby_code = code[-4:]
        return list(Players.objects.filter(code = lobby_code))

        # return Players.objects.exclude(name=name).filter(code=code)

def add_words():
    words= "alligator, america, angle, ant, applause, apple, arch, arm, army, artist, avocado, baby, backbone, bag, baker, ball, band, baseball, basin, basket, bath, bathroom, battery, bed, bedbug, bee, beehive, bell, berry, bicycle, bird, birthday cake, birthday, blade, bleach, board, boat, bomb, bone, bonnet, book, boot, bottle, bow tie, box, boy, brain, brake, branch, brick, bridge, bruise, brush, bucket, bulb, button, cabin, cake, camera, card, cardboard, carriage, cart, cat, ceiling, chain, chalk, chameleon, charger, cheerleader, cheese, chef, chess, chime, chin, church, circle, circus, cliff, cloak, clock, cloud, coach, coal, coat, collar, comb, comedian, computer, convertible, cord, cow, cowboy, cruise, crust, cup, cupcake, curtain, cushion, darts, deep, dent, dentist, diving, dog, doghouse, door, doormat, drain, drawer, dream, dress, drip, drop, dust, ear, egg, electricity, engine, extension cord, eye, face, farm, feather, finger, firefighter, fireman, fish, fizz, flag, flagpole, floor, flute, fly, fog, foot, fork, fowl, frame, french fries, frog, garbage, garden, garfield, gate, giant, girl, glove, goat, goblin, golden retriever, gun, hair dryer, hair, hammer, hand, handle, hat, head, headphones, heart, hockey, hook, hopscotch, horn, horse, hospital, hot dog, hot tub, house, houseboat, hurdle, internet, island, jewel, joke, kettle, key, knee, kneel, knife, knight, knot, koala, lace, lap, lawnmower, leaf, leak, leg, light bulb, lighthouse, line, lip, lock, mailman, map, mascot, match, mattress, money, monkey, moon, mouth, muscle, mushroom, music, nail, nature, neck, needle, neet, nerve, net, newspaper, nightmare, nose, nut, oar, office, orange, outside, oven, owl, pajamas, parcel, park, password, peach, pen, pencil, pharmacist, photograph, picnic, picture, pig, pilot, pin, pineapple, ping pong, pinwheel, pipe, pirate, plane, plank, plate, plough, pocket, pool, popsicle, post office, pot, potato, prison, pump, puppet, purse, queen, quilt, raft, rail, raincoat, rat, ray, receipt, ring, rod, roof, root, rug, safe, sail, salmon, salt and pepper, sandbox, scale, school, scissors, screw, season, seed, shallow, shampoo, sheep, sheets, shelf, ship, shirt, shoe, shrink, skate, ski, skin, skirt, sleep, snake, sneeze, snowball, sock, song, spade, speakers, sponge, spoon, spring, sprinkler, square, stamp, star, state, station, stem, stick, stingray, stocking, stomach, store, street, suitcase, sun, sunburn, sushi, swamp, sweater, table, tail, teapot, thief, think, thread, throat, thumb, ticket, time machine, tiptoe, toe, tongue, tooth, town, train, tray, treasure, tree, trip, trousers, turtle, tusk, tv, umbrella, violin, wall, watch, watering can, wax, wedding dress, wheel, whip, whistle, wig, window, wing, wire, worm, yardstick, zoo"
    word_list = words.split(sep=", ")
    word_dict = {}
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

    word_ = {}

    for i in word_list:
                Words.objects.create(word = i, point_value = word_dict[i])

    return list(Words.objects)

def get_words():
    random_key = random.choice(list(Words.objects.keys()))
    random_value = Word.objects[random_key]
    print(f'Random value: {random_value}. Random key: {random_key}')
    return random_value, random_key

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
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type, "pic": text_data_json["pic"]})
        elif action_type == "start_game":
            await self.channel_layer.group_send(self.room_group_name, {"type": action_type})
        elif action_type == "see_words":
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
    
    async def see_words(self, event):
        await self.send(text_data=json.dumps({"type": "see_words"}))
        add_words()
        words = await sync_to_async(get_words)
        #print(users)

        # await self.send(text_data=json.dumps({"type": "delete_players"}))

        # print("users", users)
        for word in words:
            # print(user.name)
            # name = user.values()["name"]
            await self.send(text_data=json.dumps({"type": "see_words", "word": word.word, "value": word.point_value}))

        