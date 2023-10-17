from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from account.models import Staff, Member, User
from academy.models import Comment, Answer


def home(request):
  return render(request, "staff/index.html")


def staff_profile(request):

  user = request.user

  context = {
    "user": user,
    "staff": user, 
  }

  return render(request, "staff/staff_profile.html", context)


@csrf_exempt
def edit_staff(request):

  if request.method == "GET": 
    user = request.user

    context = {
      'user': user,
      "staff": user,
    }

    return render(request, "staff/edit_staff.html", context)
  
  elif request.method == 'POST':
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    profile_pic = request.FILES.get("profile_pic")

    try:
      user_id = request.user.id
      staff = User.objects.get(id=user_id)
      staff.first_name = first_name
      staff.last_name = last_name
      staff.email = email
      staff.username = username

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
      return redirect('staff_profile')
    except:
      messages.error(request, 'Filed to edit!')
      return redirect('staff_profile')


def reset_staff_profile_pic(request):
  user = request.user
  try:
    user.staff.profile_pic.delete()
    messages.success(request, "Your profile picture was deleted succsessfully!")
    return redirect("edit_staff")
  except:
    messages.error(request, "There was an error while deleting your profile picture!")
    return redirect("edit_staff")


def comments(request):

  comments = Comment.objects.all()

  context = {
    "comments": comments,
  }

  return render(request, "staff/comments.html", context)


def delete_comment(request, comId):
  comment = Comment.objects.get(id=comId)

  try:
    comment.delete()
    messages.success(request, "Comment was deleted successfully!")
    return redirect("staff.comments")
  except:
    messages.error(request, "There was an error while deleting this comment!")
    return redirect("staff.comments")


@csrf_exempt
def answer(request, comId):

  if request.method == 'GET':
    comment = Comment.objects.get(id=comId)

    answers = Answer.objects.filter(comment=comment)

    context = {
      "comment": comment,
      "answers": answers,
    }

    return render(request, "staff/answer.html", context)
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
      return redirect("staff.answer", comId=comId)
    except:
      messages.error(request, "There was an error while sending your answer!")
      return redirect("staff.answer", comId=comId)


def delete_answer(request, comId, ansId):
  answer = Answer.objects.get(id=ansId)

  try:
    answer.delete()
    messages.success(request, "Answer was deleted successfully!")
    return redirect("staff.answer", comId=comId)
  except:
    messages.error(request, "There was an error while deleting this answer!")
    return redirect("staff.answer", comId=comId)

