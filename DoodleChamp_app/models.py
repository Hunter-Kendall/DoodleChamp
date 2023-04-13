from django.db import models

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
    host = models.TextField()

class Players(models.Model):
    id = models.AutoField(
                auto_created = True,
                primary_key = True,
                serialize = False, 
                verbose_name ='ID')
    code = models.ForeignKey(Lobby, default=1, on_delete=models.CASCADE)
    name = models.TextField()
    isDrawer = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
class Game(models.Model):
    code = models.ForeignKey(Lobby, default=1, on_delete=models.CASCADE)
    round = models.IntegerField(default= 2) #will count backwards
    timer = models.IntegerField(default= 90) #in seconds
    active_word = models.TextField(default = "")
    point_value = models.IntegerField(default = 0)

# class Guess(models.Model):
#     code = models.ForeignKey(Lobby, default=1, on_delete=models.CASCADE)
    




    
