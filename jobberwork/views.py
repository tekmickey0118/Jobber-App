from django.shortcuts import get_object_or_404
from django.utils import timezone

from .serializers import *
from .models import *
from users.models import User

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import *

#all specific individual detail view tasks
class IndividualTaskView(generics.ListAPIView):

    queryset = NewTask.objects.all()
    serializer_class = IndividualTaskSerializer
    model = NewTask

    def get_queryset(self):
        queryset1 = NewTask.objects.filter(id = self.kwargs['id'])
        return queryset1


#user specific tasks
class UserIndividualTaskView(generics.ListAPIView):

    queryset = NewTask.objects.all()
    serializer_class = IndividualTaskSerializer
    model = NewTask
    lookup_field = 'id'

    def get_queryset(self):
        queryset1 = NewTask.objects.filter(user = self.request.user, id = self.kwargs['id'])
        return queryset1

    def delete(self, request, *args, **kwargs):
        delete_task = self.get_object()
        delete_task.delete()
        return Response({'message':'task delete successfully'})


#user edit view serialiser
class UserEditIndividualTaskView(generics.ListAPIView):

    queryset = NewTask.objects.all()
    serializer_class = IndividualTaskSerializer
    model = NewTask
    lookup_field = 'id'

    def get_queryset(self):
        queryset1 = NewTask.objects.filter(user = self.request.user, id = self.kwargs['id'])
        return queryset1
    
    def patch(self, request, *args, **kwargs):
        task_id = self.get_object()
        serializer = IndividualTaskSerializer(task_id ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status':'200','message':'User task edited successfully'})


#shows all user tasks posted
class UserAllTaskView(generics.ListAPIView):
    queryset = NewTask.objects.all()
    serializer_class = AllTaskSerializer

    def get_queryset(self):
        task_get = NewTask.objects.filter(user = self.request.user).order_by('-id')
        return task_get


#shows all tasks
class AllTaskView(generics.ListAPIView):
    queryset = NewTask.objects.all()
    serializer_class = AllTaskSerializer

    def get_queryset(self):
        task_get = NewTask.objects.filter().order_by('-id')
        return task_get


#creates new task
class NewTaskView(APIView):
    queryset = NewTask.objects.all()
    serializer_class = NewTaskSerializer

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['active'] = True
        request.data._mutable = False
        serializer = NewTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'message':'user_task_created successfully'})
