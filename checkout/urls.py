from django.urls import path
from checkout.views import stripe_transaction, stripe_config
from checkout.views import *
from checkout.webhooks import stripe_webhook

urlpatterns = [
    # path("order/", make_order, name="checkout.order"),
    path("stripe", stripe_transaction, name="checkout.stripe"),
    path("stripe/config/", stripe_config, name="checkout.stripe.config"),
    path("stripe/webhook", stripe_webhook),
    # path("paypal/", paypal_transaction, name="checkout.paypal"),
]
