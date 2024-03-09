from django.shortcuts import render

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