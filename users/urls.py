
from django.urls import path
from .views import GoogleLogin
from . import views
from dj_rest_auth.views import LogoutView
from django.conf.urls import url

urlpatterns = [
    path('auth/google/', GoogleLogin.as_view()),
    path('logout/', LogoutView.as_view()),
]
