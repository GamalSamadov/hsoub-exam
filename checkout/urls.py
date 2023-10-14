from django.urls import path
from checkout.views import stripe_transaction, stripe_config
from checkout.views import *

urlpatterns = [
    # path("order/", make_order, name="checkout.order"),
    path("stripe/config", stripe_config, name="checkout.stripe.config"),
    path("stripe", stripe_transaction, name="checkout.stripe"),
    # path("paypal/", paypal_transaction, name="checkout.paypal"),
]
