from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    path('detalhe/<int:pk>/', detail),
    path('home/', home),
]
