from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("course/<int:id>/", course_details, name="academy.course_details"),
    path("questions/", questions, name="questions"),
    path("books/", books, name="books"),
    path("store/", store, name="store"),
    path("store/courses/", store_courses, name="store.courses"),
    path("store/course/<int:id>/", store_course_details, name="academy.store.course.details"),
    path("store/cart/", cart, name="academy.store.cart"),
    path("store/cart/add/<int:cid>/", cart_update, name="academy.store.cart_add"),
    path("store/cart/remove/<int:cid>/", cart_remove, name="academy.store.cart.remove"),
    path("checkout/", checkout, name="academy.checkout"),
    path("checkout/complete/", checkout_complate, name="academy.checkout.complate"),
]
