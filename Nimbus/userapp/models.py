from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    cityID= models.AutoField(primary_key=True, blank=False)
    name = models.CharField(max_length=25)
    class Meta:
        db_table = 'cities'

class Users(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table= "Users"