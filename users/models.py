from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=255, null=False)
    profile_pic =
    email = models.EmailField(max_length=255, unique=True)
    reg_no. = models.TextField(max_length = 9)
    hostel_room = models.TextField()
    phone = models.IntegerField(max_length = 12)
    gender = models.CharField()
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

