from django.urls import path
from HOD.views import *

urlpatterns = [
    path('', home, name="hod_home"),
    path('profile/', admin_profile, name="admin_profile"),
    path('profile/edit/', edit_admin, name="edit_admin"),
    path('profile/reset_profile_picture/', reset_admin_profile_pic, name="reset_admin_profile_pic"),

    path('staffs/', staffs, name="staffs"),
    path('add_staff/', add_staff, name="add_staff"),
    path('staff/<int:id>/', staff_profile, name="staff_profile"),
    path('staff/<int:id>/edit/', edit_staff, name="edit_staff"),
    path('staff/<int:id>/reset_profile_picture/', reset_staff_profile_pic, name="reset_staff_profile_pic"),
    path('staff/<int:id>/delete/', delete_staff, name="delete_staff"),

    path('members/', members, name="members"),
    path('add_member/', add_member, name="add_member"),
    path('member/<int:id>/', member_profile, name="member_profile"),
    path('member/<int:id>/edit/', edit_member, name="edit_member"),
    path('member/<int:id>/delete/', delete_member, name="delete_member"),
    path('member/<int:id>/reset_member_profile_pic/', reset_member_profile_pic, name="reset_member_profile_pic"),
    path('member/<int:id>/ban/', ban_member, name="ban_member"),
    path('member/<int:id>/activate/', activate_member, name="activate_member"),

    path("courses/", courses, name="courses"),
    path("add_course/", add_course, name="add_course"),
    path("course/<int:id>", course_profile, name="course_profile"),
    path("course/<int:id>/edit/", edit_course, name="edit_course"),
    path("course/<int:id>/delete/", delete_course, name="delete_course"),
    path("course/<int:id>/add_subtitle/", add_course_subtitle, name="add_course_subtitle"),
    path("course/<int:courseId>/subtitle/<int:subtitleId>/", course_subtitle_profile, name="course_subtitle_profile"),
    path("course/<int:courseId>/subtitle/<int:subtitleId>/edit/", edit_course_subtitle, name="edit_course_subtitle"),
    path("course/<int:courseId>/subtitle/<int:subtitleId>/delete/", delete_course_subtitle, name="delete_course_subtitle"),
    path("course/<int:courseId>/subtitle/<int:subtitleId>/add_video/", add_course_video, name="add_course_video"),
    path("course/<int:courseId>/subtitle/<int:subtitleId>/video/<int:videoId>/", course_video_profile, name="course_video_profile"),
    path("course/<int:courseId>/subtitle/<int:subtitleId>/video/<int:videoId>/edit/", edit_course_video, name="edit_course_video"),
    path("course/<int:courseId>/subtitle/<int:subtitleId>/video/<int:videoId>/delete/", delete_course_video, name="delete_course_video"),

    path("orders/", orders, name="hod.orders"),
    path("orders/approve/<int:oid>", approve_order, name="hod.order.approve"),

]
