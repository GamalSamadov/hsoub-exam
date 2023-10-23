from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.translation import gettext as _
from academy.models import Course, CourseSubTitle, Cart, Order, CourseVideo, Comment, Answer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


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


@login_required(login_url="/account/login")
def cart(request):
  context = {

  }

  return render(request, "academy/cart.html", context)


@login_required(login_url="/account/login")
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


@login_required(login_url="/account/login")
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


@login_required(login_url="/account/login")
def checkout(request):

  context = {

  }

  return render(request, "academy/checkout.html", context)


@login_required(login_url="/account/login")
def checkout_complate(request):
  Cart.objects.filter(session=request.session.session_key).delete()
  return render(request, "academy/checkout_complate.html")


@login_required(login_url="/account/login")
def my_courses(request):

  user = request.user

  orders = Order.objects.filter(transaction__customer__id=user.id)

  courses = []
  for order in orders:
    for order_course in order.ordercourse_set.filter(approved=True):
      courses.append(order_course.course)
  
  # count_videos = 0

  # for course in courses:
  #   for subtitle in course.coursesubtitle_set.all():
  #     count_videos += subtitle.coursevideo_set.all().count()
  context = {
    "courses": courses,
    # "count_videos": count_videos,
  }

  return render(request, "academy/my_courses.html", context)


@login_required(login_url="/account/login")
def subtitles(request, cid):

  course = Course.objects.get(id=cid)

  subtitles = CourseSubTitle.objects.filter(course__id=cid)

  context = {
    "course": course,
    "subtitles": subtitles,

  }

  return render(request, "academy/subtitles.html", context)


@login_required(login_url="/account/login")
def videos(request, cid, sid):

  course = Course.objects.get(id=cid)

  subtitle = CourseSubTitle.objects.get(id=sid)

  videos = CourseVideo.objects.filter(subtitle__id=sid)

  context = {
    "course": course,
    "subtitle": subtitle,
    "videos": videos,
  }

  return render(request, "academy/videos.html", context)


@login_required(login_url="/account/login")
def video(request, cid, sid, vid):

  course = Course.objects.get(id=cid)
  subtitle = CourseSubTitle.objects.get(id=sid)
  video = CourseVideo.objects.get(id=vid)
  comments = Comment.objects.filter(video=video)

  context = {
    "course": course,
    "subtitle": subtitle,
    "video": video,
    "comments": comments,
  }

  return render(request, "academy/video.html", context)


@login_required(login_url="/account/login")
@csrf_exempt
def add_comment(request, cid, sid, vid):

  if request.method == "POST":
    user = request.user
    video = CourseVideo.objects.get(id=vid)
    text = request.POST.get("text")
    if text is not None:
      try:
        Comment.objects.create(
          sender=user,
          video=video,
          text=text,
        )
        messages.success(request, "Comment added! Will be approved soon!")
        return redirect("academy.video", cid=cid, sid=sid, vid=vid)
      except:
        messages.error(request, "There was an error while adding your comment!")
        return redirect("academy.video", cid=cid, sid=sid, vid=vid)
    else:
        messages.error(request, "This field can not be empty!")
        return redirect("academy.video.add_comment", cid=cid, sid=sid, vid=vid)



@login_required(login_url="/account/login")
def answers(request, cid, sid, vid, comId):
  course = Course.objects.get(id=cid)
  subtitle = CourseSubTitle.objects.get(id=sid)
  video = CourseVideo.objects.get(id=vid)
  comment = Comment.objects.get(id=comId)
  answers = Answer.objects.filter(comment=comment)

  context = {
    "course": course,
    "subtitle": subtitle,
    "video": video,
    "comment": comment,
    "answers": answers,
  }

  return render(request, "academy/answers.html", context) 


@login_required(login_url="/account/login")
@csrf_exempt
def add_answer(request, cid, sid, vid, comId):

  if request.method == "POST":
    user = request.user
    comment = Comment.objects.get(id=comId)

    text = request.POST.get("text")
    try:
      Answer.objects.create(
        comment=comment,
        sender=user,
        text=text,
      )
      messages.success(request, "Your answer added successfully!")
      return redirect("academy.video.answers", cid=cid, sid=sid, vid=vid, comId=comId)
    except:
      messages.error(request, "There was an error while adding your answer!")
      return redirect("academy.video.answers", cid=cid, sid=sid, vid=vid, comId=comId)


