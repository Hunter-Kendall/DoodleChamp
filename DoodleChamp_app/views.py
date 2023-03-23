from django.shortcuts import render
from DoodleChamp_app.models import Lobby
import string
import random

# Create your views here.

def index(request):
    return render(request, "game/index.html")

def room_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) 
    room_filter = Lobby.objects.filter(code = room_code)
    if len(room_filter.values()) == 0:
        return code
    else:
        return room_code()

# Make this be what gets called by create_lobby url. Drop room_name.
def lobby(request):
    # Randomly generate a room name.
    code = room_code()
    Lobby.objects.create(code = code, host = request.POST["name"])

    # Pass in the room name (or room_id) and the user_name to be rendered on the page.
    return render(request, "game/lobby.html", {"room_name": code})#this is where we set room id
    # In lobby.html, have the websocket connect and pass withit the room_id and user_name.
    # In the consumer, create a group for this game.
    # Coordinate communications between websockets and javascript.
    # Each websocket (user) has a unique channel_name.


def game_room(request, game_room_name):
    return render(request, "game/game.html", {"game_room_name": game_room_name})