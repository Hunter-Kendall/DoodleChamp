from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "game/index.html")

def room(request, room_name):
    return render(request, "game/lobby.html", {"room_name": room_name})