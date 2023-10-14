from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="staff_home")
]
