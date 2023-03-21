from django.db import models

class Words(models.Model):
    id = models.AutoField(
                  auto_created = True,
                  primary_key = True,
                  serialize = False, 
                  verbose_name ='ID')
    word = models.TextField()
    point_value = models.IntegerField()
