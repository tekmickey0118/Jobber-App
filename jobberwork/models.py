from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField


class NewTask(models.Model):
    user = models.ForeignKey(User,related_name = 'user_requested',on_delete = models.CASCADE)
    Title = models.TextField(null=False)
    Description = models.TextField(null=False)
    Time = models.TimeField()
    Date = models.DateField()
    location = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.Title

class UserAssigned(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    delivery_user = models.OneToOneField(User, related_name = 'user_delivery', on_delete = models.CASCADE)
    task = models.OneToOneField(NewTask, related_name='user_assigned', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.task.Title


class UserPending(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    task = models.OneToOneField(NewTask, related_name='user_pending', on_delete=models.CASCADE)
    pending = models.BooleanField(default=False)

    def __str__(self):
        return self.task.Title

class UserCompleted(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    task = models.OneToOneField(NewTask, related_name='user_completed', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task.Title


