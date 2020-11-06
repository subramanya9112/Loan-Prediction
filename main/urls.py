from django.contrib import admin
from django.urls import path
from .views import home, logOut

urlpatterns = [
    path('', home, name="home"),
    path('Logout', logOut, name="logout"),
]
