# Generated by Django 4.2.6 on 2023-10-11 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0003_rename_sub_title_coursesubtitle_subtitle"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coursevideo",
            old_name="sub_title",
            new_name="subtitle",
        ),
    ]
