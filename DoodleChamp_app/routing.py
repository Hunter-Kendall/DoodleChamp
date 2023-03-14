from django.urls import re_path

from DoodleChamp_app import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.DoodleChamp_appConsumer.as_asgi()),
]