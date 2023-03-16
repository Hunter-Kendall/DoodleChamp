from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "game/index.html")

def room(request, room_name):
    return render(request, "game/lobby.html", {"room_name": room_name})

def game_room(request, game_room_name):
    return render(request, "game/game.html", {"game_room_name": game_room_name})