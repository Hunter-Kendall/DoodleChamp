from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return str(self.username)

class Stats(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    wins = models.IntegerField()
    loses = models.IntegerField()

class Stats(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    wins = models.IntegerField()
    loses = models.IntegerField()


class Words(models.Model):
    id = models.AutoField(
                auto_created = True,
                primary_key = True,
                serialize = False, 
                verbose_name ='ID')
    word = models.TextField()
    point_value = models.IntegerField()

class Lobby(models.Model):
    code = models.TextField(primary_key = True)
    host = models.ForeignKey(User, on_delete=models.PROTECT)

class Players(models.Model):
    id = models.AutoField(
                auto_created = True,
                primary_key = True,
                serialize = False, 
                verbose_name ='ID')
    code = models.ForeignKey(Lobby, default=1, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.PROTECT)
    isDrawer = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
class Game(models.Model):
    code = models.ForeignKey(Lobby, default=1, on_delete=models.CASCADE)
    round = models.IntegerField(default= 2) #will count backwards
    timer = models.IntegerField(default= 90) #in seconds
    active_word = models.TextField(default = "")
    point_value = models.IntegerField(default = 0)