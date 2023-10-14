# Generated by Django 4.2.6 on 2023-10-11 18:42

import academy.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0004_rename_sub_title_coursevideo_subtitle"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="pic",
            field=models.ImageField(upload_to=academy.models.Course.upload_file_name),
        ),
        migrations.AlterField(
            model_name="coursevideo",
            name="video",
            field=models.FileField(
                upload_to=academy.models.CourseVideo.upload_file_name
            ),
        ),
    ]
