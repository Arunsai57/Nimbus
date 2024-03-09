from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=25, unique=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'cities'

class Users(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    mobile= models.CharField(max_length=10)
    img= models.ImageField(upload_to="")
    gender= models.CharField(max_length=10)
    
    class Meta:
        db_table= "Users"