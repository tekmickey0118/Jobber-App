from rest_framework.response import Response
from .models import User
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

        if self.user.username == '':
            check = {'username_exists': False}
        else:
            check = {'username_exists': True}
        response = Response({**serializer.data, **check}, status=status.HTTP_200_OK)
        return response


class CustomSocialLoginView(CustomLoginView):
    serializer_class = SocialLoginSerializer


class GoogleLogin(CustomSocialLoginView):
    permission_classes = ()
    adapter_class = GoogleOAuth2Adapter
    token_model = TokenModel
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        url = self.request.data.get('callback_url')
        self.callback_url = url
        return super(GoogleLogin, self).post(request, *args, **kwargs)


@api_view(['POST'])
def user_form(request):
    if User.objects.filter(username=request.data['username']).exists():
        return Response({'error': 'User with this username already exists'})
    else:
        serializer = UserFormSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp = {"success": "information saved successfully"}
        return Response(resp)


@api_view(['GET'])
def user_detail_view(request):
    serializer = UserInfoSerializer(request.user)
    return Response(serializer.data)


from django.core.files.uploadedfile import UploadedFile
@api_view(['PATCH','GET'])
def user_edit(request, format = None):
    if request.method == 'PATCH':
        if User.objects.filter(username=request.data['username']).exists():
            return Response({'error': 'User with this username already exists'})
        else:
            serializer = UserEditSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            resp = {"success": "Information saved successfully"}
            return Response(resp)
    if request.method == 'GET':
        serializer = UserEditSerializer(request.user)
        return Response(serializer.data)