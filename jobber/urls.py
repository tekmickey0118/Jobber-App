from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/work/', include('jobberwork.urls')),

]
