from django.shortcuts import render
from DoodleChamp_app.models import Lobby, Players, Game, Stats
import string
import random

from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Stats.objects.create(user = user, wins = 0, loses = 0)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")
# Create your views here.

def index(request):
    lobbies = Lobby.objects.all() # To be removed. Only for testing purposes
    return render(request, "game/home.html", {'lobbies': lobbies})

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
    username = request.user
    code = room_code()
    Lobby.objects.create(code = code, host = username)
    lobby_code = Lobby.objects.get(code = code)
    Players.objects.create(code = lobby_code, name = username, isDrawer = True)
    Game.objects.create(code = lobby_code)

    # Pass in the room name (or room_id) and the user_name to be rendered on the page.
    return render(request, "game/lobby_host.html", {"room_name": code, "username": username.username})#this is where we set room id
    # In lobby.html, have the websocket connect and pass withit the room_id and user_name.
    # In the consumer, create a group for this game.
    # Coordinate communications between websockets and javascript.
    # Each websocket (user) has a unique channel_name.


def game_room(request):
    
    return render(request, "game/game.html", {"game_room_name": request.POST["game-code"], "username": request.POST["username"]})
    

def join_lobby(request):
    lobby_code = request.POST["code"]
    username = request.user
    lobby_filter = Lobby.objects.filter(code = lobby_code)
    name_check = Players.objects.filter(code = lobby_code, name = username)
    if len(lobby_filter.values()) == 1:
        if len(name_check.values()) == 1:
            return render(request, "game/lobby.html", {"room_name": lobby_code, "username": username})
        else:
            code = Lobby.objects.get(code = lobby_code)
            Players.objects.create(code = code, name = username)
            return render(request, "game/lobby.html", {"room_name": lobby_code, "username": username})
    else:
        pass
