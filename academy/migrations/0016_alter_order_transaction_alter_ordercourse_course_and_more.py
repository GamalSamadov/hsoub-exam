# Generated by Django 4.2.6 on 2023-10-17 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0004_alter_transaction_customer"),
        ("academy", "0015_remove_comment_approved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="transaction",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="checkout.transaction",
            ),
        ),
        migrations.AlterField(
            model_name="ordercourse",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="academy.course",
            ),
        ),
        migrations.AlterField(
            model_name="ordercourse",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="academy.order",
            ),
        ),
    ]
