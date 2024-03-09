from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('card', views.card, name='card'),
    path('box',views.box,name="box"),
     path('guide', views.guide, name='guide'),
]
