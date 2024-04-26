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
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    cities = models.ManyToManyField(City)
    mobile= models.CharField(max_length=10)
    img= models.ImageField(upload_to="")
    
    class Meta:
        db_table= "Users"

class Forecast(models.Model):
    city_name = models.CharField(max_length=100)
    forecast_date = models.DateField()
    forecast_time = models.TimeField()
    temperature = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.city_name} - {self.forecast_date} {self.forecast_time}'
    
