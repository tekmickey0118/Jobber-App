from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=255, null=False)
    profile_pic = models.ImageField(upload_to = '', blank = True)
    email = models.EmailField(max_length=255, unique=True)
    reg_number = models.TextField(max_length = 9)
    hostel_room = models.TextField()
    phone = models.IntegerField(default = None, null = True)
    gender = models.TextField()
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class User_status(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    deliveries_done = models.IntegerField()

    def __str__(self):
        return self.Title