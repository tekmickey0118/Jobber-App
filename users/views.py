from rest_framework.response import Response
from .models import User, UserReview, User_status
from rest_framework.decorators import api_view
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.models import TokenModel
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.views import LoginView
from rest_framework import status
from django.conf import settings
from .serializers import *
import base64
import os
from django.core.files import File 
from django.core.files.uploadedfile import UploadedFile
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model


class CustomLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
            }
            serializer = serializer_class(
                instance=data, context=self.get_serializer_context()
            )
        else:
            serializer = serializer_class(
                instance=self.token, context=self.get_serializer_context()
            )
        domain_false = {'domain_vit': False}
        domain_true= {'domain_vit': True}

        #user exist validation
        if self.user.username:
            check = {'user_exists': True}
        else:
            check = {'user_exists': False}

        if self.user.email.split('@')[1] == "vitstudent.ac.in":
            response = Response({**serializer.data, **check,**domain_true}, status=status.HTTP_200_OK)
            logged_in_user = User.objects.get(id = self.request.user.id)
            logged_in_user.username = self.user.email
            logged_in_user.first_name = logged_in_user.first_name.title()
            logged_in_user.reg_number = self.user.last_name
            logged_in_user.save(update_fields=['username','reg_number'])
        else:
            response = Response({**serializer.data, **domain_false}, status=status.HTTP_200_OK)
            User.objects.get(id = self.request.user.id).delete()
        return response


class CustomSocialLoginView(CustomLoginView):
    serializer_class = SocialLoginSerializer


class GoogleLogin(CustomSocialLoginView):
    permission_classes = ()
    adapter_class = GoogleOAuth2Adapter
    token_model = TokenModel
    client_class = OAuth2Client
    callback_url = "https://127.0.0.1:8000/"


@api_view(['GET','PATCH'])
def user_form(request):
    if request.method == 'PATCH':
        serializer = UserFormSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp = {"success": "information saved successfully"}
        return Response(resp)
    if request.method == 'GET':
        serializer = UserFormSerializer(request.user)
        return Response(serializer.data)


@api_view(['GET'])
def user_detail_view(request):
    serializer = UserInfoSerializer(request.user)
    return Response(serializer.data)


@api_view(['PATCH','GET'])
def user_edit(request, format = None):
    """
    description: This API deletes/uninstalls a device.
    """
    if request.method == 'PATCH':
        serializer = UserEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp = {"success": "Information saved successfully"}
        return Response(resp)
    if request.method == 'GET':
        serializer = UserEditSerializer(request.user)
        return Response(serializer.data)

'''
@api_view(['GET'])
def username_exists(request):
    if request.user.username:
        return Response({"username_exists": True})
    else:
        return Response({"username_exists": False})
'''

'''
@api_view(['GET'])
def reg_exists(request):
    if request.user.reg_number:
        return Response({"reg_exists": True})
    else:
        return Response({"reg_exists": False})
'''


#user specific tasks
class UserIndividualView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    queryset = User.objects.all()
    serializer_class = IndividualUserSerializer
    model = User
    lookup_field = 'first_name'

    def get_queryset(self):
        queryset1 = User.objects.filter(first_name = self.kwargs['first_name'])
        return queryset1
        
        
        
