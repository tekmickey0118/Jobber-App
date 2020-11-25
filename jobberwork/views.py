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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = NewTask.objects.all()
    serializer_class = IndividualTaskSerializer
    model = NewTask

    def get_queryset(self):
        queryset1 = NewTask.objects.filter(id = self.kwargs['id'])
        return queryset1


#user specific tasks
class UserIndividualTaskView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = NewTask.objects.all()
    serializer_class = AllTaskSerializer

    def get_queryset(self):
        task_get = NewTask.objects.filter(user = self.request.user).order_by('-id')
        return task_get


#shows all tasks
class AllTaskView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    queryset = NewTask.objects.all()
    serializer_class = AllTaskSerializer

    def get_queryset(self):
        task_get = NewTask.objects.filter().order_by('-id')
        return task_get


#creates new task
class NewTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = NewTask.objects.all()
    serializer_class = NewTaskSerializer

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['active'] = True
        request.data._mutable = False
        
        self.request.user.total_tasks += 1
        
        serializer = NewTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'message':'user_task_created successfully'})


#requesting to accept the task
class AcceptedTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        
        accept_task_id = int(request.data['task_id'])
        tasks = NewTask.objects.get(pk = accept_task_id)
        
        if tasks.active:
            tasks.active = False
            assigned_object = UserAssigned.objects.create(user = tasks.user, delivery_user = self.request.user, task = tasks)
            pending_object = UserPending.objects.create(user = tasks.user, task = tasks, pending = True)

            assigned_object.save()
            pending_object.save()
            tasks.save(update_fields=['active'])
            return Response({'message':'Accepted this Request'})

        else:
            return Response({'This task has already been accepted..'})


#accepted_Task_view for user
class PendingTaskUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = NewTask.objects.all()
    serializer_class = PendingTaskSerializer

    def get_queryset(self):
        delivery_user_tasks = NewTask.objects.filter(user_pending__pending = True)
        return (delivery_user_tasks)


#accepted_Task_view for user
class MyAcceptedTaskView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = NewTask.objects.all()
    serializer_class = PendingTaskSerializer

    def get_queryset(self):
        delivery_user_tasks = NewTask.objects.filter(user_assigned__delivery_user = self.request.user.id ,user_pending__pending = True)
        return (delivery_user_tasks)


#complete or close task request
class CompletedTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        accept_task_id = int(request.data['task_id'])
        tasks = NewTask.objects.get(pk = accept_task_id)
        assigned_task = UserPending.objects.get(task_id = accept_task_id)

        if not tasks.active:
            assigned_task.pending = False
            completed_object = UserCompleted.objects.create(user = tasks.user, task = tasks, completed = True)

            completed_object.save()

            self.request.user.completed_tasks += 1
            assigned_task.save(update_fields=['pending'])
            return Response({'message':'Task Completed successfully'})

        else:
            return Response({'message':'Task has already been completed'})


#Completed_Task_view for user
class CompletedTaskUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = NewTask.objects.all()
    serializer_class = CompletedTaskSerializer

    def get_queryset(self):
        delivery_user_tasks = NewTask.objects.filter(user_completed__completed = True)
        return (delivery_user_tasks)


#cancel task request
class CancelTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        accept_task_id = int(request.data['task_id'])
        tasks = NewTask.objects.get(pk = accept_task_id)
        assigned_task = UserPending.objects.get(task_id = accept_task_id)

        if not tasks.active:
            assigned_task.pending = False
            completed_object = UserCompleted.objects.create(user = tasks.user, task = tasks, completed = False)

            completed_object.save()

            self.request.user.uncompleted_tasks += 1
            assigned_task.save(update_fields=['pending'])
            return Response({'message':'Task Cancelled Completed successfully'})
        
        else:
            return Response({'message':'Task is not active'}) #workding can be made better


#Uncompleted_Task_view for user
class UncompletedTaskUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = NewTask.objects.all()
    serializer_class = CompletedTaskSerializer

    def get_queryset(self):
        delivery_user_tasks = NewTask.objects.filter(user_completed__completed = False)
        return (delivery_user_tasks)

