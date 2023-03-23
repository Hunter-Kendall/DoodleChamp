from django.shortcuts import render
from DoodleChamp_app.models import Lobby

# Create your views here.

def index(request):
    return render(request, "game/index.html")

# Make this be what gets called by create_lobby url. Drop room_name.
def lobby(request, room_name):
    # Randomly generate a room name.
    Lobby.objects.create(code = "room_id", host = request.POST["name"])
    # Pass in the room name (or room_id) and the user_name to be rendered on the page.
    return render(request, "game/lobby.html", {"room_name": request.POST["name"]})#this is where we set room id
    # In lobby.html, have the websocket connect and pass withit the room_id and user_name.
    # In the consumer, create a group for this game.
    # Coordinate communications between websockets and javascript.
    # Each websocket (user) has a unique channel_name.


def game_room(request, game_room_name):
    return render(request, "game/game.html", {"game_room_name": game_room_name})