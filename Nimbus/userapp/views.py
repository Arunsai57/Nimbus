import datetime
import json
from pyexpat.errors import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
from .forms import CityForm
from .models import City, Forecast, Users
from django.contrib.auth import models, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def index(request):     
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'Non-User/Landing.html')

def home(request):
    API_KEY = '63407539ca53a7ee84abeced0dabbbb9'

        #ip
    ip = requests.get('https://api.ipify.org?')
    ip_text= ip.text
    res = requests.get('http://ip-api.com/json/'+ip_text)
    location_data_one = res.text
    location_data = json.loads(location_data_one)
    place= location_data.get('city')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = '{:.1f}'.format(data['main']['temp'] - 273.15)
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        city, created = City.objects.get_or_create(
            name=place,
            defaults={'temperature': temperature, 'humidity': humidity, 'description': description}
        )
    return render(request, 'User/Home.html', {'city': city})

def box(request):
    return render(request,"User/box.html")
  
def guide(request):
    return render(request,'User/guide.html')

def map(request):
    return render(request,'User/map.html')

def search(request):
    if request.user.is_authenticated:
        user_profile = Users.objects.get(user=request.user)
        user_cities = user_profile.cities.all()
        return render(request, 'User/search.html', {'user_cities': user_cities})

    return render(request, 'User/search.html')

def user_signup(request):
    if request.method == 'POST':
        first_name= request.POST['first-name']
        last_name= request.POST['last-name']
        username = request.POST['username']
        email= request.POST['email']
        password = request.POST['password']
        password1= request.POST['confirm-password']

        if password != password1:
            messages.error(request,"Passwords do not match!!")
            return redirect('signup')
        try:
            user= models.User.objects.create_user(first_name= first_name, last_name= last_name, username= username, email= email, password= password)
            users= Users.objects.create(user= user)
            users.save()
            return redirect("login")
        except IntegrityError as e:
            messages.error(request, 'Username is already taken. Please choose a different one.')
            print(e)
            return redirect('signup')
        
    return render(request, "User/signup.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials!!')
            return redirect('login')
    return render(request, "User/Login.html")

def feedback(request):
    if request.method== "POST":
        name= request.POST['name']
        subject = request.POST['subject']
        recipient_address= []
        recipient_address.append(request.POST['email'])
        message = request.POST['message'] + "Email from user: " + request.POST['email']
        email_from = settings.EMAIL_HOST_USER
        admin_mail= settings.EMAIL_SITE_ADMIN
        send_mail(subject, message, email_from, [admin_mail])
        subject= "Hello "+ name+"!"
        message= "We are so sorry to hear that our services aren't up to your standard but we stand on a promise to strive to make a better website for you. We have recieved your email and we will use your message to better ourselves"
        send_mail(subject, message, email_from, recipient_address)
        return redirect('home')
    return render(request, 'Feedback.html')

def addCity(request):
    if request.user.is_authenticated:
        API_KEY = '63407539ca53a7ee84abeced0dabbbb9'
        current_user = Users.objects.get(user=request.user)
        weather_data = current_user.cities.all()

        place = request.POST.get('city', '')
        if place:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                temperature = '{:.1f}'.format(data['main']['temp'] - 273.15)
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']

                city, created = City.objects.get_or_create(
                    name=place,
                    defaults={'temperature': temperature, 'humidity': humidity, 'description': description}
                )

                current_user.cities.add(city)

                return render(request, 'User/search.html', {'saved_weather_data': weather_data})
            else:
                error_message = 'City not found. Please try again.'
                return render(request, 'User/search.html', {'error_message': error_message, 'saved_weather_data': weather_data})
    else:
        place = request.POST.get('city', '')
        API_KEY = '63407539ca53a7ee84abeced0dabbbb9'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}'
        response = requests.get(url)

        data = response.json()
        temperature = '{:.1f}'.format(data['main']['temp'] - 273.15)
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        return render(request, 'User/search.html', {'weather_data':{'city': str.upper(place), 'temperature': temperature, 'humidity': humidity, 'description': description}})
    
def user_logout(request):
    if request.user.is_authenticated:
        auth_logout(request) 
    return redirect('index')

def get_5_day_forecast(place):
    API_KEY = '63407539ca53a7ee84abeced0dabbbb9'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast_data = {}
        for forecast in data['list']:
            forecast_date = forecast['dt_txt'].split()[0]
            forecast_time = forecast['dt_txt'].split()[1]
            temperature = '{:.1f}'.format(forecast['main']['temp'] - 273.15)
            humidity = forecast['main']['humidity']
            description = forecast['weather'][0]['description']
            if forecast_date not in forecast_data:
                forecast_data[forecast_date] = []
            forecast_data[forecast_date].append({
                'time': forecast_time,
                'temperature': temperature,
                'humidity': humidity,
                'description': description
            })
        save_forecast_to_db(place ,forecast_data)
        return forecast_data
    else:
        return None

def save_forecast_to_db(place, data):
    for forecast_date, forecasts in data.items():
        for forecast in forecasts:
            Forecast.objects.create(
                city_name=place,
                forecast_date=datetime.datetime.strptime(forecast_date, '%Y-%m-%d').date(),
                forecast_time=datetime.datetime.strptime(forecast['time'], '%H:%M:%S').time(),
                temperature=float(forecast['temperature']),
                humidity=int(forecast['humidity']),
                description=forecast['description']
            )


def showCity(request):
    if request.method == 'POST':
        place = request.POST.get('city_name', '')
        forecast = get_5_day_forecast(place)
        if forecast:
            return render(request, 'User/show_city.html', {'forecast_data': forecast, 'city_name': place})
        else:
            error_message = 'City not found. Please try again.'
            return render(request, 'User/show_city.html', {'error_message': error_message})
    else:
        return redirect('search')


# def addCity(request):
#         if request.user.is_authenticated:
#             current_user = Users.objects.get(user=request.user)
#             weather_data = current_user.objects.all()
#         place = request.POST.get('city', '')
#         if place:
#             API_KEY = '63407539ca53a7ee84abeced0dabbbb9'
#             url = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}'
#             response = requests.get(url)

#             if response.status_code == 200:
#                 data = response.json()
#                 temperature = '{:.1f}'.format(data['main']['temp'] - 273.15)
#                 humidity = data['main']['humidity']
#                 description = data['weather'][0]['description']

#                 # city = current_user.cities.get_or_create(
#                 #     name=place,
#                 #     defaults={'temperature': temperature, 'humidity': humidity, 'description': description}
#                 # )

#                 return render(request, 'User/search.html', {'weather_data':{'city': str.upper(place), 'temperature': temperature, 'humidity': humidity, 'description': description}},{'saved_weather_data': weather_data})
#             else:
#                 error_message = 'City not found. Please try again.'
#                 return render(request, 'User/search.html', {'error_message': error_message, 'saved_weather_data': weather_data})
