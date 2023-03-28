from django.shortcuts import render
from DoodleChamp_app.models import Lobby, Players
import string
import random

# Create your views here.

def index(request):
    return render(request, "game/index.html")

def room_code():
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) 
    room_filter = Lobby.objects.filter(code = random_code)
    if len(room_filter.values()) == 0:
        return random_code
    else:
        return room_code()

# Make this be what gets called by create_lobby url. Drop room_name.
def create_lobby(request):
    # Randomly generate a room name.
    code = room_code()
    username = request.POST["name"]
    Lobby.objects.create(code = code, host = username)
    lobby_code = Lobby.objects.get(code = code)
    Players.objects.create(code = lobby_code, name = username)

    # Pass in the room name (or room_id) and the user_name to be rendered on the page.
    return render(request, "game/lobby.html", {"room_name": code, "username": username})#this is where we set room id
    # In lobby.html, have the websocket connect and pass withit the room_id and user_name.
    # In the consumer, create a group for this game.
    # Coordinate communications between websockets and javascript.
    # Each websocket (user) has a unique channel_name.


def game_room(request, game_room_name):
    # return render(request, "game/game.html", {"game_room_name": game_room_name})
    pass 

def join_lobby(request):
    lobby_code = request.POST["code"]
    username = request.POST["name"]
    lobby_filter = Lobby.objects.filter(code = lobby_code)
    if len(lobby_filter.values()) == 1:
        code = Lobby.objects.get(code = lobby_code)
        Players.objects.create(code = code, name = username)
        return render(request, "game/lobby.html", {"room_name": lobby_code, "username": username})
    else:
        pass
