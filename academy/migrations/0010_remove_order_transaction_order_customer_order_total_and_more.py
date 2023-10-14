# Generated by Django 4.2.6 on 2023-10-13 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("academy", "0009_rename_card_cart"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="transaction",
        ),
        migrations.AddField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="total",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="ordercourse",
            name="price",
            field=models.IntegerField(null=True),
        ),
    ]
