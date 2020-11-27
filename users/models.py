from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
import urllib.request
import mimetypes

class User(AbstractUser):

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_NON_BINARY = 'N'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male', ), 
        (GENDER_FEMALE, 'Female', ), 
        (GENDER_NON_BINARY, 'Non Binary', ),
    )

    username = models.CharField(max_length=255, null=False)
    profile_pic = models.ImageField(upload_to = '', blank = True)
    email = models.EmailField(max_length=255, unique=True)
    reg_number = models.TextField(max_length = 9, unique = True) #capitals
    hostel_room = models.TextField()
    phone = models.CharField(max_length = 12)
    gender = models.TextField(choices=GENDER_CHOICES)
    total_tasks = models.IntegerField(default = 0)
    completed_tasks = models.IntegerField(default = 0)
    uncompleted_tasks = models.IntegerField(default = 0)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save_profile_pic(user):
        url = username
        filename = user.id + mimettypes.guess_extension(urllib.request.urlopen(url).headers['content-type'])
        path = os.path.join(settings.MEDIA_ROOT, filename)

        urllib.request.urlretrieve(url, path)

        user.image = path
        user.save()

#to put tasks integer field to this model----------
class User_status(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    deliveries_done = models.IntegerField()

    def __str__(self):
        return self.Title