from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name="home"),

    path('login/', views.user_login , name="login"),

    path('register/', views.register, name="register"),

    path('hotel_detail/<uuid:uid>', views.detail, name='detail'),
    
]

