from django.contrib import admin

from .models import *

admin.site.register(NewTask)
admin.site.register(UserPending)
admin.site.register(UserCompleted)
