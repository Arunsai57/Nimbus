from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'Non-User/Landing.html')

def home(request):
    return render(request, 'User/Home2.html')

def guide(request):
    return render(request,'User/guide.html')