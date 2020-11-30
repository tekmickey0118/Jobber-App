
from django.urls import path
from .views import GoogleLogin
from . import views
from dj_rest_auth.views import LogoutView
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('auth/google/', GoogleLogin.as_view()),
    path('me/form/', views.user_form),
    path('me/info/', views.user_detail_view),
    path('me/edit/', views.user_edit),
    path('<str:first_name>', views.UserIndividualView.as_view()),
    path('logout/', LogoutView.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)