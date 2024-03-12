from pyexpat.errors import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
from .forms import CityForm
from .models import City, Users
from django.contrib.auth import models, authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'Non-User/Landing.html')

def home(request):
    return render(request, 'User/Home.html')

def box(request):
    return render(request,"User/box.html")
  
def guide(request):
    return render(request,'User/guide.html')

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
                temperature = '{:.1f}'.format(data['main']['temp'] - 273.15)
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

    return render(request, 'User/search.html', {'weather_data': weather_data})

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
            users.save()
            return redirect("login")
        except IntegrityError as e:
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('signup')
        
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
            messages.error(request, "Invalid Credentials!!")
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