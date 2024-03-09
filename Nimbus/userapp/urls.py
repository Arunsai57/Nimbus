from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('guide', views.guide, name='guide'),
    path('map', views.map, name='map'),
    # path('search', views.search, name='search'),
    path('box',views.box,name="box"),
     path('guide', views.guide, name='guide'),
    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
]
