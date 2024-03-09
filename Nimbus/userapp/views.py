from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'Non-User/Landing.html')

def home(request):
    return render(request, 'User/Home.html')
def card(request):
    return render(request, 'Card.html')
def box(request):
    return render(request,"User/box.html")
  
def guide(request):
    return render(request,'User/guide.html')
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
    