from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from hsoub import settings
from academy.models import Course, Cart, Course, Order
from account.models import User
from checkout.models import Transaction, PaymentMethod
from checkout.forms import UserInfoForm
import math, stripe


# def make_order(request):
#   if request.method != "POST":
#     return redirect("academy.checkout")
  
#   elif request.method == "POST":
#     print("========= Hiiiii")
#     cart = Cart.objects.filter(session=request.session.session_key)
#     courses = Course.objects.filter(pk__in=cart.items)

#     total = 0

#     for item in courses:
#       total += item.price

#     if total <= 0:
#       return redirect("academy.store.cart")
    
#     user = request.user
#     order = Order.objects.create(customer=user, total=total)
#     print(order, "======== order")

#     for course in courses:
#       order.ordercourse_set.create(course_id=course.id, price=course.price)
#       print(course.title, "================== course")
#       print(order.ordercourse_set.price, "============== order course price",)

#     cart.delete()
#     return redirect("home")



def stripe_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


@csrf_exempt
def stripe_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Stripe)
    if not transaction:
        return JsonResponse({
            'message': _('Please enter valid information.')
        }, status=400)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=transaction.amount * 100,
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={
            'transaction': transaction.id
        }
    )
    return JsonResponse({
        'client_secret': intent['client_secret']
    })


# def paypal_transaction(request):
#     transaction = make_transaction(request, PaymentMethod.Paypal)
#     if not transaction:
#         return JsonResponse({
#             'message': _('Please enter valid information.')
#         }, status=400)

#     form = MyPayPalPaymentsForm(initial={
#         'business': settings.PAYPAL_EMAIL,
#         'amount': transaction.amount,
#         'invoice': transaction.id,
#         'currency_code': settings.CURRENCY,
#         'return_url': f'http://{request.get_host()}{reverse("store.checkout_complete")}',
#         'cancel_url': f'http://{request.get_host()}{reverse("store.checkout")}',
#         'notify_url': f'http://{request.get_host()}{reverse("checkout.paypal-webhook")}',
#     })

#     return HttpResponse(form.render())


@csrf_exempt
def make_transaction(request, pm):

    cart = Cart.objects.filter(session=request.session.session_key).last()
    courses = Course.objects.filter(pk__in=cart.items)

    total = 0
    for item in courses:
        total += item.price

    if total <= 0:
        return None

    user = request.user
    user_model = User.objects.get(id=user.id)
    return Transaction.objects.create(
        customer=user_model,
        session=request.session.session_key,
        payment_method=pm,
        items=cart.items,
        amount=math.ceil(total)
    )