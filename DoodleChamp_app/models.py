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
    
