from django.db import models
from django.utils.translation import gettext as _
from account.models import User

class TransactionStatus(models.IntegerChoices):
  Pending = 0, _("Pending")
  Complated = 1, _("Complated")


class PaymentMethod(models.IntegerChoices):
  Stripe = 1, _("Stripe")
  Paypal = 2, _("Paypal")


class Transaction(models.Model):
  session = models.CharField(max_length=255)
  amount = models.IntegerField()
  items = models.JSONField(default=dict)
  customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  status = models.IntegerField(
    choices=TransactionStatus.choices,
    default=TransactionStatus.Pending,
  )
  payment_method = models.IntegerField(
    choices=PaymentMethod.choices,
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  @property
  def customer_name(self):
    return f"{self.customer['first_name']} {self.customer['last_name']}"
  
  @property
  def customer_email(self):
    return self.customer['email']