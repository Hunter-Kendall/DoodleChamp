# DoodleChamp_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Home", views.index, name="home"),
    path("Host", views.create_lobby, name="lobby"),
    #path("<str:room_name>/", views.lobby, name="lobby"),
    # path("<str:game_room_name>/", views.game_room, name="game_room"),
    path("Lobby", views.join_lobby, name="join"),
    path("Game", views.game_room, name="game_room"),
    # path("Lobby/Game", views.game_room, name="game_room")
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
]