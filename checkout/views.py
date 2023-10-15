from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from hsoub import settings
from academy.models import Course, Cart, Course, Order
from account.models import User
from checkout.models import Transaction, PaymentMethod
from checkout.forms import UserInfoForm
from django.contrib.auth.decorators import login_required
import math, stripe


@login_required(login_url="/account/login")
def stripe_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


@login_required(login_url="/account/login")
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


@login_required(login_url="/account/login")
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
