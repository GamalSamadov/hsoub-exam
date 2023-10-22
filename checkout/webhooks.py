from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from hsoub.settings import STRIPE_ENDPOINT_SECRET
from django.http import HttpResponse
from checkout.models import Transaction
from academy.models import Order, Course
import stripe, json


# @require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        print('Error parsing payload: {}'.format(str(e)))
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print('Error verifying webhook signature: {}'.format(str(e)))
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
      # print('PaymentIntent was successful!')
      payment_intent = event.data.object
      transaction_id = payment_intent.metadata.transaction
      make_order(transaction_id)
    
    elif event.type == 'payment_method.attached':
      print('PaymentMethod was attached to a Customer!')

    else:
      print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)



def make_order(transaction_id):
   transaction = Transaction.objects.get(pk=transaction_id)

   order = Order.objects.create(transaction=transaction)

   courses = Course.objects.filter(pk__in=transaction.items)

   for course in courses:
      order.ordercourse_set.create(course_id=course.id, price=course.price)
    
    
