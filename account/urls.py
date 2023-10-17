from django.urls import path
from account.views import *

urlpatterns = [
    path("", index, name="account_main"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", register, name="register"),
    path("banned/", banned, name="banned"),
]
