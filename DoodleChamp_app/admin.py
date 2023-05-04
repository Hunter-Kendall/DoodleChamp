from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from DoodleChamp_app.models import User, Lobby, Players, Words, Game, Stats

admin.site.register(User, UserAdmin)
admin.site.register(Lobby)
admin.site.register(Players)
admin.site.register(Words)
admin.site.register(Game)
admin.site.register(Stats)


