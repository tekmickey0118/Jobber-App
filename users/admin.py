from django.contrib import admin

from .models import User, User_status, UserReview

admin.site.register(User)
admin.site.register(User_status)
admin.site.register(UserReview)
