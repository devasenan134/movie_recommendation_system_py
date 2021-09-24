from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('logout', views.logoutuser, name="logoutuser"),
    path('login', views.loginuser, name="loginuser"),
    path("signup", views.signupuser, name="signupuser"),
]
