from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from account.models import Staff, Member, User
from academy.models import Course, CourseSubTitle, CourseVideo, OrderCourse, Comment, Answer


# Home
def home(request):

  user = request.user

  staffs = Staff.objects.all()
  members = Member.objects.all()

  courses = Course.objects.all()

  context = {
    'user' : user,
    "staffs_count": staffs.count(),
    "members_count": members.count(),
    "courses": courses,
  }

  return render(request, "HOD/index.html", context)


# Admin
def admin_profile(request):

  user = request.user

  context = {
    "user": user,
    "admin": user, 
  }

  return render(request, "HOD/admin_profile.html", context)


@csrf_exempt
def edit_admin(request):

  if request.method == "GET": 
    user = request.user

    context = {
      'user': user,
      "admin": user,
    }

    return render(request, "HOD/edit_admin.html", context)
  
  elif request.method == 'POST':
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    profile_pic = request.FILES.get("profile_pic")

    try:
      user_id = request.user.id
      admin = User.objects.get(id=user_id)
      admin.first_name = first_name
      admin.last_name = last_name
      admin.email = email
      admin.username = username

      if password != "" and password != None:
        admin.set_password(password)
      
      if profile_pic:
        if admin.admin.profile_pic:
          admin.admin.profile_pic.delete()
          admin.admin.profile_pic = profile_pic
        else:
          admin.admin.profile_pic = profile_pic

      admin.admin.save()
      admin.save()
      messages.success(request, 'Edited successfully.')
      return redirect('admin_profile')
    except:
      messages.error(request, 'Filed to edit!')
      return redirect('admin_profile')


def reset_admin_profile_pic(request):
  user = request.user
  try:
    user.admin.profile_pic.delete()
    messages.success(request, "Your profile picture was deleted succsessfully!")
    return redirect("edit_admin")
  except:
    messages.error(request, "There was an error while deleting your profile picture!")
    return redirect("edit_admin")


# Staff
def staffs(request):
  user = request.user

  staffs = Staff.objects.all()

  context = {
    'user' : user,
    "staffs": staffs,
  }

  return render(request, "HOD/staffs.html", context)


@csrf_exempt
def add_staff(request):

  if request.method == "GET": 
    user = request.user

    context = {
      'user': user,
    }

    return render(request, "HOD/add_staff.html", context)
  
  elif request.method == 'POST':
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    profile_pic = request.FILES.get("profile_pic")

    try:
      user = User.objects.create_user(
          first_name=str(first_name).capitalize().strip(),
          last_name=str(last_name).capitalize().strip(),
          email=str(email).lower().strip(),
          username=str(username).lower().strip(),
          password=password,
          user_type=2,
          )
      if profile_pic:
        user.staff.profile_pic = profile_pic
        user.save()
      messages.success(request, 'Added successfully.')
      return redirect('staffs')
    except:
      messages.error(request, 'Filed to add!')
      return redirect('staffs')


def staff_profile(request, id):

  user = request.user
  staff = User.objects.get(id=id)

  context = {
    "user": user,
    "staff": staff, 
  }

  return render(request, "HOD/staff_profile.html", context)


@csrf_exempt
def edit_staff(request, id):

  if request.method == "GET": 
    user = request.user
    staff = User.objects.get(id=id)

    context = {
      'user': user,
      "staff": staff,
    }

    return render(request, "HOD/edit_staff.html", context)
  
  elif request.method == 'POST':
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    profile_pic = request.FILES.get("profile_pic")

    try:
      staff = User.objects.get(id=id)
      staff.first_name = str(first_name).capitalize().strip()
      staff.last_name = str(last_name).capitalize().strip()
      staff.email = str(email).lower().strip()
      staff.username = str(username).lower().strip()

      if password != "" and password != None:
        staff.set_password(password)
      
      if profile_pic:
        if staff.staff.profile_pic:
          staff.staff.profile_pic.delete()
          staff.staff.profile_pic = profile_pic
        else:
          staff.staff.profile_pic = profile_pic
          
      staff.staff.save()
      staff.save()
      messages.success(request, 'Edited successfully.')
      return redirect('staff_profile', id=id)
    except:
      messages.error(request, 'Filed to edit!')
      return redirect('staff_profile', id=id)


def reset_staff_profile_pic(request, id):
  staff = Staff.objects.get(user=id)
  try:
    staff.profile_pic.delete()
    messages.success(request, "Staff profile picture was deleted succsessfully!")
    return redirect("staff_profile", id=id)
  except:
    messages.error(request, "There was an error while deleting staff profile picture!")
    return redirect("staff_profile", id=id)


def delete_staff(request, id):
    staff = User.objects.get(id=id)

    try:
      staff.delete()
      messages.success(request, "Staff deleted successfully!")
      return redirect("staffs")
    except:
      messages.success(request, "Staff deleted successfully!")
      return redirect("staffs")


# Member
def members(request):
  user = request.user

  members = Member.objects.all()

  context = {
    'user' : user,
    "members": members,
  }

  return render(request, "HOD/members.html", context)


@csrf_exempt
def add_member(request):

  if request.method == "GET": 
    user = request.user

    context = {
      'user': user,
    }

    return render(request, "HOD/add_member.html", context)
  
  elif request.method == 'POST':
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    profile_pic = request.FILES.get("profile_pic")

    try:
      user = User.objects.create_user(
          first_name=str(first_name).capitalize().strip(),
          last_name=str(last_name).capitalize().strip(),
          email=str(email).lower().strip(),
          username=str(username).lower(),
          password=password,
          user_type=3,
          )
      if profile_pic:
        user.member.profile_pic = profile_pic
      
      user.save()
      messages.success(request, 'Added successfully.')
      return redirect('members')
    except:
      messages.error(request, 'Filed to add!')
      return redirect('members')


def member_profile(request, id):

  user = request.user
  member = User.objects.get(id=id)

  context = {
    "user": user,
    "member": member, 
  }

  return render(request, "HOD/member_profile.html", context)


@csrf_exempt
def edit_member(request, id):

  if request.method == "GET": 
    user = request.user
    member = User.objects.get(id=id)

    context = {
      'user': user,
      "member": member,
    }

    return render(request, "HOD/edit_member.html", context)
  
  elif request.method == 'POST':
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    profile_pic = request.FILES.get("profile_pic")

    try:
      member = User.objects.get(id=id)
      member.first_name = first_name
      member.last_name = last_name
      member.email = email
      member.username = username

      if password != "" and password != None:
        member.set_password(password)

      if profile_pic:
        if member.member.profile_pic:
          member.member.profile_pic.delete()
          member.member.profile_pic = profile_pic
        else:
          member.member.profile_pic = profile_pic

      member.member.save()
      member.save()
      messages.success(request, 'Edited successfully.')
      return redirect('member_profile', id=id)
    except:
      messages.error(request, 'Filed to edit!')
      return redirect('member_profile', id=id)


def reset_member_profile_pic(request, id):
  member = Member.objects.get(user=id)
  try:
    member.profile_pic.delete()
    messages.success(request, "Member profile picture was deleted succsessfully!")
    return redirect("member_profile", id=id)
  except:
    messages.error(request, "There was an error while deleting member profile picture!")
    return redirect("member_profile", id=id)


def delete_member(request, id):
    member = User.objects.get(id=id)

    try:
      member.delete()
      messages.success(request, "Member deleted successfully!")
      return redirect("members")
    except:
      messages.success(request, "Member deleted successfully!")
      return redirect("members")


def ban_member(request, id):
  member = Member.objects.get(user=id)
  try: 
    member.banned = True
    member.save()
    messages.success(request, "Member was banned successfully!")
    return redirect("edit_member", id=id)
  except:
    messages.error(request, "Can't ban this Member!")
    return redirect("edit_member", id=id)
  

def activate_member(request, id):
  member = Member.objects.get(user=id)
  try: 
    member.banned = False
    member.save()
    messages.success(request, "Member was activated successfully!")
    return redirect("edit_member", id=id)
  except:
    messages.error(request, "Can't activate this Member!")
    return redirect("edit_member", id=id)


# Course
def courses(request):

  user = request.user

  courses = Course.objects.all()

  context = {
    'user': user,
    'courses': courses,
  }

  return render(request, "HOD/courses.html", context)


@csrf_exempt
def add_course(request):
  
  if request.method == "GET": 
    user = request.user

    context = {
      'user': user,
    }

    return render(request, "HOD/add_course.html", context)
  
  elif request.method == 'POST':
    title = request.POST.get("title")
    description = request.POST.get("description")
    pic = request.FILES.get("pic")
    price = request.POST.get("price")

    try:
      Course.objects.create(
        title=title,
        description=description,
        price=price,
        pic=pic,
      )
      messages.success(request, 'Added successfully.')
      return redirect('courses')
    except:
      messages.error(request, 'Filed to add!')
      return redirect('courses')


def course_profile(request, id):
  user = request.user
  course = Course.objects.get(id=id)

  subtitles = CourseSubTitle.objects.filter(course=course)

  context = {
    "user": user,
    "course": course, 
    "subtitles": subtitles,
  }

  return render(request, "HOD/course_profile.html", context)


@csrf_exempt
def edit_course(request, id):

  if request.method == "GET": 
    user = request.user
    course = Course.objects.get(id=id)

    context = {
      'user': user,
      "course": course,
    }

    return render(request, "HOD/edit_course.html", context)
  
  elif request.method == 'POST':
    title = request.POST.get("title")
    description = request.POST.get("description")
    pic = request.FILES.get("pic")
    price = request.POST.get("price")

    try:
      course = Course.objects.get(id=id)
      course.title = title
      course.description = description
      course.price = price
      if pic:
        if course.pic:
          course.pic.delete()
          course.pic = pic
        else:
          course.pic = pic

      course.save()
      messages.success(request, 'Edited successfully.')
      return redirect('course_profile', id=id)
    except:
      messages.error(request, 'Filed to edit!')
      return redirect('course_profile', id=id)


def delete_course(request, id):

  course = Course.objects.get(id=id)

  try:
    course.delete()
    messages.success(request, "Deleted successfully!")
    return redirect("courses")
  except:
    messages.error(request, "There was an error")
    return redirect("courses")


@csrf_exempt
def add_course_subtitle(request, id):

  if request.method == "GET":
    user = request.user
    course = Course.objects.get(id=id)

    context = {
      'user': user,
      "course": course,
    }

    return render(request, "HOD/add_course_subtitle.html", context)
  elif request.method == "POST":
    course = Course.objects.get(id=id)
    try:
      subtitle = request.POST.get("subtitle")
      CourseSubTitle.objects.create(
        subtitle=subtitle,
        course=course,
      )
      messages.success(request, "Subtitle added successfully!")
      return redirect("course_profile", id=id)
    except:
      messages.error(request, "There was an problem while adding subtitle!")
      return redirect("course_profile", id=id)


def course_subtitle_profile(request, courseId, subtitleId):
  user = request.user
  course = Course.objects.get(id=courseId)
  subtitle = CourseSubTitle.objects.get(id=subtitleId)
  videos = CourseVideo.objects.filter(subtitle=subtitle)

  context = {
    'user': user,
    "course": course,
    "subtitle": subtitle,
    "videos": videos,
  }

  return render(request, "HOD/course_subtitle_profile.html", context)


@csrf_exempt
def edit_course_subtitle(request, courseId, subtitleId):

  if request.method == "GET":
    user = request.user
    course = Course.objects.get(id=courseId)
    subtitle = CourseSubTitle.objects.get(id=subtitleId)

    context = {
      'user': user,
      "course": course,
      "subtitle": subtitle,
    }

    return render(request, "HOD/edit_course_subtitle.html", context)
  elif request.method == "POST":
    course = Course.objects.get(id=courseId)
    subtitle = CourseSubTitle.objects.get(id=subtitleId)
    try:
      subtitle_subtitle = request.POST.get("subtitle")
      
      subtitle.subtitle = subtitle_subtitle
      subtitle.save()

      messages.success(request, "Subtitle added successfully!")
      return redirect("course_subtitle_profile", courseId=courseId, subtitleId=subtitleId)
    except:
      messages.error(request, "There was an problem while adding subtitle!")
      return redirect("course_subtitle_profile", courseId=courseId, subtitleId=subtitleId)


def delete_course_subtitle(request, courseId, subtitleId):
  subtitle = CourseSubTitle.objects.get(id=subtitleId)
  try:
    subtitle.delete()
    messages.success(request, "Subtitle deleted successfully!")
    return redirect("course_profile", id=courseId)
  except:
    messages.error(request, "There was a problem!")
    return redirect("course_profile", id=courseId)


@csrf_exempt
def add_course_video(request, courseId, subtitleId):
  if request.method == "GET":

    course = Course.objects.get(id=courseId)
    subtitle = CourseSubTitle.objects.get(id=subtitleId)

    context = {
      "course": course,
      "subtitle": subtitle,
    }

    return render(request, "HOD/add_course_video.html", context)
  if request.method == 'POST':
    subtitle = CourseSubTitle.objects.get(id=subtitleId)
    title = request.POST.get("title")
    description = request.POST.get("description")
    video = request.FILES.get("video")
    try:
      CourseVideo.objects.create(
        subtitle=subtitle,
        description=description,
        title=title,
        video=video,
      )
      messages.success(request, "Video added successfully!")
      return redirect("course_subtitle_profile", courseId=courseId, subtitleId=subtitleId)
    except:
      messages.error(request, "There was an error!")
      return redirect("course_subtitle_profile", courseId=courseId, subtitleId=subtitleId)


def course_video_profile(request, courseId, subtitleId, videoId):

  user = request.user
  course = Course.objects.get(id=courseId)
  subtitle = CourseSubTitle.objects.get(id=subtitleId)
  video = CourseVideo.objects.get(id=videoId)

  context = {
    "user": user,
    "course": course,
    "subtitle": subtitle,
    "video": video,
  }

  return render(request, "HOD/course_video_profile.html", context)


@csrf_exempt
def edit_course_video(request, courseId, subtitleId, videoId):

  if request.method == 'GET':
    course = Course.objects.get(id=courseId)

    subtitle = CourseSubTitle.objects.get(id=subtitleId)

    video = CourseVideo.objects.get(id=videoId)

    context = {
      "course": course,
      "subtitle": subtitle,
      "video": video,
    }

    return render(request, "HOD/edit_course_video.html", context)
  elif request.method == 'POST':
    title = request.POST.get("title")
    description = request.POST.get("description")
    video = request.FILES.get("video")
    try:
      course_video = CourseVideo.objects.get(id=videoId) 
      course_video.title = title
      course_video.description = description
      course_video.video = video
      
      course_video.save()
      messages.success(request, "Edited successfully!")
      return redirect("course_video_profile", courseId=courseId, subtitleId=subtitleId, videoId=videoId)
    except:
      messages.error(request, "Failed to edit!")
      return redirect("course_video_profile", courseId=courseId, subtitleId=subtitleId, videoId=videoId)


def delete_course_video(request, courseId, subtitleId, videoId):

  video = CourseVideo.objects.get(id=videoId)

  try:
    video.delete()
    messages.success(request, "Video deleted successfully!")
    return redirect("course_subtitle_profile", courseId=courseId, subtitleId=subtitleId)
  except:
    messages.error(request, "Failed to delete video!")
    return redirect("course_subtitle_profile", courseId=courseId, subtitleId=subtitleId)


def orders(request):

  orders = OrderCourse.objects.all()

  context = {
    "orders": orders,
  }

  return render(request, "HOD/orders.html", context)


def approve_order(request, oid):

  order = OrderCourse.objects.get(id=oid)

  try:
    order.approved = True
    order.save()
    messages.success(request, "The order was been approved!")
    return redirect("hod.orders")
  
  except:
    messages.error(request, "There was error while approving the order!")
    return redirect("hod.orders")


def comments(request):

  comments = Comment.objects.all()

  context = {
    "comments": comments,
  }

  return render(request, "HOD/comments.html", context)


def delete_comment(request, comId):
  comment = Comment.objects.get(id=comId)

  try:
    comment.delete()
    messages.success(request, "Comment was deleted successfully!")
    return redirect("hod.comments")
  except:
    messages.error(request, "There was an error while deleting this comment!")
    return redirect("hod.comments")


@csrf_exempt
def answer(request, comId):

  if request.method == 'GET':
    comment = Comment.objects.get(id=comId)

    answers = Answer.objects.filter(comment=comment)

    context = {
      "comment": comment,
      "answers": answers,
    }

    return render(request, "HOD/answer.html", context)
  elif request.method == "POST":
    sender = request.user
    comment = Comment.objects.get(id=comId)

    text = request.POST.get("text")

    try:
      Answer.objects.create(
        sender=sender,
        comment=comment,
        text=text,
      )
      messages.success(request, "Your answer was sended successfully!")
      return redirect("hod.answer", comId=comId)
    except:
      messages.error(request, "There was an error while sending your answer!")
      return redirect("hod.answer", comId=comId)


def delete_answer(request, comId, ansId):
  answer = Answer.objects.get(id=ansId)

  try:
    answer.delete()
    messages.success(request, "Answer was deleted successfully!")
    return redirect("hod.answer", comId=comId)
  except:
    messages.error(request, "There was an error while deleting this answer!")
    return redirect("hod.answer", comId=comId)

