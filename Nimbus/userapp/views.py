from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
from .forms import CityForm
from .models import City, Users
from django.contrib.auth import models, authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'Non-User/Landing.html')

def home(request):
    return render(request, 'User/Home.html')

def box(request):
    return render(request,"User/box.html")
  
def guide(request):
    return render(request,'User/guide.html')

def signup(request):
    return render(request,"User/signup.html")

def login(request):
    return render(request,"User/Login.html")

def map(request):
    return render(request,'User/map.html')

def search(request):
    weather_data = City.objects.all()

    if request.method == 'POST':
        place = request.POST.get('city', '')

        if place:
            API_KEY = '63407539ca53a7ee84abeced0dabbbb9'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                temperature = data['main']['temp']
                temperature= temperature-273.15
                temperature= '{:.1f}'.format(temperature)    
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']

                city, created = City.objects.get_or_create(
                    name=place,
                    defaults={'temperature': temperature, 'humidity': humidity, 'description': description}
                )

                return render(request, 'User/search.html', {'city': city, 'weather_data': weather_data})
            else:
                error_message = 'City not found. Please try again.'
                return render(request, 'User/search.html', {'error_message': error_message, 'weather_data': weather_data})
            
    for i in weather_data:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={i.name}&appid=63407539ca53a7ee84abeced0dabbbb9')
        if response.status_code == 200:
                data = response.json()
                temperature = data['main']['temp']
                temperature= temperature-273.15
                temperature= '{:.1f}'.format(temperature)    
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']

                city = City.objects.get(name= i.name)
                city.temperature= temperature
                city.humidity= humidity
                city.description= description
                city.save()
    return render(request, 'User/search.html', {'weather_data': weather_data})


# def search(request):
#     if request.method == 'POST':
#         place = requests.POST['place']
#         API_KEY = '63407539ca53a7ee84abeced0dabbbb9'
#         url = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}'
#         response = request.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             print(data)
#             temperature = data['main']['temp']
#             humidity = data['main']['humidity']
#             temperature1 = round(temperature - 273.15, 2)
#             return render(request, 'User/search.html',
#                           {'city': str.upper(place), 'temperature1': temperature1, 'humidity': humidity})
#         else:
#             error_message = 'City not found. Please try again.'
#             return render(request, 'User/search.html', {'error_message': error_message})
#     return render(request,"UseWr/search.html")
    