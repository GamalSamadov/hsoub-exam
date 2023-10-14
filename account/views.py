from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from account.models import *
from account.EmailBackEnd import EmailBackEnd
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return redirect("login")


@csrf_exempt
def user_login(request):
    if request.method != "POST":
        return render(request, "account/login.html")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                messages.success(request, 'Welcome back to admin panel')
                return redirect('hod_home')

            elif user_type == '2':
                messages.success(request, 'Welcome back to staff panel')
                return redirect('staff_home')

            elif user_type == '3':
                messages.success(request, 'Welcome back')
                return redirect('home')
            else:
                messages.error(request, "Can not login")
                return redirect('login')
        else:
            messages.error(request, "Email or password is wrong, try again!")
            return redirect('login')


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request, 'account/register.html')    
   
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.create_user(
                first_name=str(first_name).capitalize().strip(),
                last_name=str(last_name).capitalize().strip(),
                email=str(email).lower().strip(),
                username=str(username).lower(),
                password=password,
                user_type=3,
                )
            user.save()
            messages.success(request, 'You have registered up successfully.')
            return redirect('home')
        except:
            messages.error(request, 'Failed to register')
            return redirect('home')


def user_logout(request):
    print(request.user.username, "Logged out")
    logout(request)
    return HttpResponseRedirect('/')