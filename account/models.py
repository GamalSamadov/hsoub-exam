from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models



class User(AbstractUser):
  user_type_data = ((1, "Admin"), (2, "Staff"), (3, "Member"))
  user_type = models.CharField(
    default=1,
    choices=user_type_data,
    max_length=10
    )

class Admin(models.Model):
  def upload_file_name(self, filename):
    return f'users/Admin/{self.user.first_name}_{self.user.last_name}/profile_pic/{filename}'
  
  id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  profile_pic = models.ImageField(upload_to=upload_file_name, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()

  def delete(self, using=None, keep_parents=False):
    self.profile_pic.delete()
    super().delete()


class Staff(models.Model):
  def upload_file_name(self, filename):
    return f'users/Staff/{self.user.first_name}_{self.user.last_name}/profile_pic/{filename}'
  
  id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  profile_pic = models.ImageField(upload_to=upload_file_name, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()

  def delete(self, using=None, keep_parents=False):
    self.profile_pic.delete()
    super().delete()


class Member(models.Model):
  def upload_file_name(self, filename):
    return f'users/Member/{self.user.first_name}_{self.user.last_name}/profile_pic/{filename}'
  
  id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  profile_pic = models.ImageField(upload_to=upload_file_name, null=True)
  banned = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()

  def delete(self, using=None, keep_parents=False):
    self.profile_pic.delete()
    super().delete()


# Creating Django Signals
# It's like trigger in database. It will run only when Data is Added in CustomUser model
@receiver(post_save, sender=User)
# Now Creating a Function which will automatically insert data in Admin, Staff or Member
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(user=instance)
        if instance.user_type == 2:
            Staff.objects.create(user=instance)
        if instance.user_type == 3:
            Member.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.member.save()