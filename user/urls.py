from django.urls import path
from . import models
from. import views

urlpatterns = [
    path('', views.userhome),
]







