from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.translation import gettext as _
from account.models import User
from academy.models import Course, CourseSubTitle, Cart


def index(request):
  user = request.user
  courses = Course.objects.all() 

  context = {
    'user' : user,
    "courses": courses,
  }
  return render(request, "academy/index.html", context)


def course_details(request, id):
    user = request.user
    course = Course.objects.get(id=id)
    subtitles = CourseSubTitle.objects.filter(course=course)
    courses = Course.objects.all()
    context = {
      "user": user,
      "course": course,
      "courses": courses,
      "subtitles": subtitles,
    }
    return render(request, "academy/course_details.html", context)


def questions(request):
  return render(request, "academy/questions.html")


def books(request):
  return render(request, "academy/questions.html")


def store(request):
  return redirect("store.courses")


def store_courses(request):

  user = request.user
  courses = Course.objects.all()

  context = {
    "user": user,
    "courses": courses,
  }

  return render(request, "academy/store.html", context)


def store_course_details(request, id):

  user = request.user
  course = Course.objects.get(id=id)

  context = {
    "user": user,
    "course": course,
  }

  return render(request, "academy/store_course_details.html", context)


def cart(request):

  context = {

  }

  return render(request, "academy/cart.html", context)


def cart_update(request, cid):

  if not request.session.session_key:
    request.session.create()

  session_id = request.session.session_key

  cart_model = Cart.objects.filter(session=session_id).last()

  if cart_model is None:
    cart_model = Cart.objects.create(session_id=session_id, items=[cid])
  
  elif cid not in cart_model.items:
    cart_model.items.append(cid)
    cart_model.save()

  return JsonResponse({
    "message": _("Course has been added to the cart!"),
    "items_count": len(cart_model.items)
  })


def cart_remove(request, cid):

  session_id = request.session.session_key

  if not session_id:
    return JsonResponse({})

  cart_model = Cart.objects.filter(session=session_id).last()

  if cart_model is None:
    return JsonResponse({})
  
  elif cid in cart_model.items:
    cart_model.items.remove(cid)
    cart_model.save()

  return JsonResponse({
    "message": _("Course has been removed to the cart!"),
    "items_count": len(cart_model.items)
  })


def checkout(request):

  context = {

  }

  return render(request, "academy/checkout.html", context)


def checkout_complate(request):
  Cart.objects.filter(session=request.session.session_key).delete()
  return render(request, "academy/index.html")