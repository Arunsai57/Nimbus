from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('guide', views.guide, name='guide'),
    path('map', views.map, name='map'),
    path('search', views.search, name='search'),
      
     
]
