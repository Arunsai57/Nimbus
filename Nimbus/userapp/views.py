from django.shortcuts import render

# Create your views here.
def index(request):
    count= 5
    context = {'count': count}
    return render(request, 'User/Landing.html', context)