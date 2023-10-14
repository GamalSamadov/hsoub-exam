from academy.models import Cart, Course


def academy_context(request):

  user = request.user

  cart = Cart.objects.filter(session=request.session.session_key).last()

  cart_total = 0
  cart_courses = []

  if cart:
    cart_courses = Course.objects.filter(pk__in=cart.items)

    for item in cart_courses:
      cart_total += item.price

  return {
    "user": user,
    "cart_courses": cart_courses,
    "cart_total": cart_total,
  }