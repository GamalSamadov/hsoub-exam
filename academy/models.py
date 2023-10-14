from django.db import models
from django.contrib.sessions.models import Session
from account.models import Member, User
from checkout.models import Transaction
import os


class Course(models.Model):
  def upload_file_name(self, filename):
    return f'courses/{self.title}/course_pic/{filename}'
  
  title = models.CharField(max_length=255)
  description = models.CharField(max_length=255, null=True)
  pic = models.ImageField(upload_to=upload_file_name)
  price = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)
  
  def delete(self, using=None, keep_parents=False):
    self.pic.delete()
    super().delete()

class CourseSubTitle(models.Model):
  subtitle = models.CharField(max_length=255)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)


class CourseVideo(models.Model):
  def upload_file_name(self, filename):
    return f'courses/{self.subtitle.course.title}/{self.subtitle.subtitle}/{self.title}/{filename}'
  
  title = models.CharField(max_length=255)
  subtitle = models.ForeignKey(CourseSubTitle, on_delete=models.CASCADE)
  video = models.FileField(upload_to=upload_file_name)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)

  def delete(self, using=None, keep_parents=False):
    self.video.delete()
    super().delete()

class MemberCourses(models.Model):
  member = models.ForeignKey(Member, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)


class Order(models.Model):
  transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)


class OrderCourse(models.Model):
  order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
  course = models.ForeignKey(Course, on_delete=models.PROTECT, null=True)
  price = models.FloatField(null=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.id
  

class Cart(models.Model):
  items = models.JSONField(default=dict)
  session = models.ForeignKey(Session, on_delete=models.CASCADE)
