# DoodleChamp_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.lobby, name="lobby"),
    path("<str:game_room_name>/", views.game_room, name="game_room")
]