from pyexpat.errors import messages
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
    
def search(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=fa0b357d0a95ed106ea6e258a4479311'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        try:
            r = requests.get(url.format(city)).json()
            city_weather = {
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }
            weather_data.append(city_weather)
        except KeyError:
            # Handle the case where expected keys are not present in the API response
            city_weather = {
                'city': city.name,
                'temperature': 'N/A',
                'description': 'N/A',
                'icon': 'N/A',
            }
            weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'User/search.html', context)

def user_signup(request):
    if request.method == 'POST':
        first_name= request.POST['first-name']
        last_name= request.POST['last-name']
        username = request.POST['username']
        email= request.POST['email']
        password = request.POST['password']
        password1= request.POST['confirm-password']

        if password != password1:
            messages.error(request,"Password does not match")
            return redirect('signup')

        user= models.User.objects.create_user(first_name= first_name, last_name= last_name, username= username, email= email, password= password)
        users= Users.objects.create(user= user)
        users.save()
        users.save()
        return redirect("login")
    return render(request, "User/signup.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request, "User/Login.html")