from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "HOD.views":
                    pass
                elif modulename == "account.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("hod_home")
            
            elif user.user_type == "2":
                if modulename == "staff.views":
                    pass
                elif modulename == "account.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("staff_home")
            
            elif user.user_type == "3":
                if modulename == "academy.views" and not user.member.banned:
                    pass
                elif modulename == "account.views" or modulename == "django.views.static" or modulename == "checkout.views" or modulename == "checkout.webhooks":
                    pass
                else:
                    if user.member.banned:
                        return redirect("banned")
                    else:
                        return redirect("home")

            else:
                return redirect("login")

        else:
            if modulename == "academy.views":
                pass
            elif modulename == "account.views" or modulename == "django.views.static" or modulename == "checkout.views" or modulename == "checkout.webhooks":
                pass
            else:
                return redirect("home")
