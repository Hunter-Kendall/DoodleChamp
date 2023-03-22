from django.shortcuts import render
from DoodleChamp_app.models import Lobby

# Create your views here.

def index(request):
    return render(request, "game/index.html")

def lobby(request, room_name):
    Lobby.objects.create(code = "room_id", host = request.POST["name"])
    return render(request, "game/lobby.html", {"room_name": request.POST["name"]})#this is where we set room id

def game_room(request, game_room_name):
    return render(request, "game/game.html", {"game_room_name": game_room_name})