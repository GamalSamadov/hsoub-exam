from django.urls import path
from staff.views import *


urlpatterns = [
    path("", home, name="staff_home"),
    path('profile/', staff_profile, name="staff_profile"),
    path('profile/edit/', edit_staff, name="edit_staff"),
    path('profile/reset_profile_picture/', reset_staff_profile_pic, name="reset_staff_profile_pic"),

    path("comments/", comments, name="staff.comments"),
    path("comments/<int:comId>/", answer, name="staff.answer"),
    path("comments/<int:comId>/delete/", delete_comment, name="staff.delete_comment"),
    path("comments/<int:comId>/answer/<int:ansId>/delete/", delete_answer, name="staff.delete_answer"),

]
