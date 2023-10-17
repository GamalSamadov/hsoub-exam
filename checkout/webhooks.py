from django.views.decorators.csrf import csrf_exempt
from hsoub.settings import STRIPE_ENDPOINT_SECRET
from django.http import HttpResponse
from checkout.models import Transaction
from academy.models import Order, Course
import stripe


@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']

  try:
      event = stripe.Webhook.construct_event(
          payload, sig_header, STRIPE_ENDPOINT_SECRET
      )
  except ValueError as e:
      return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
      return HttpResponse(status=400)

  # Handle the event
  if event.type == 'payment_intent.succeeded':
    payment_intent = event.data.object
    transaction_id = payment_intent.metadata.transaction
    make_order(transaction_id)
    print(transaction_id)

  else:
    print('Unhandled event type {}'.format(event['type']))

  return HttpResponse(status=200)


def make_order(transaction_id):
   transaction = Transaction.objects.get(pk=transaction_id)

   order = Order.objects.create(transaction=transaction)

   courses = Course.objects.filter(pk__in=transaction.items)

   for course in courses:
      order.ordercourse_set.create(course_id=course.id, price=course.price)
    
    
