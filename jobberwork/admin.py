from django.contrib import admin

from .models import *

admin.site.register(NewTask)
admin.site.register(UserAssigned)
admin.site.register(UserPending)
admin.site.register(UserCompleted)
admin.site.register(ItemPicked)
