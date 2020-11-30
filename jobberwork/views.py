from django.shortcuts import get_object_or_404
from django.utils import timezone

from .serializers import *
from .models import *
from users.models import User, User_status

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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

#all specific individual detail view tasks after accepting
class IndividualAcceptTaskView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    queryset = NewTask.objects.all()
    serializer_class = IndividualAcceptTaskSerializer
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
        if delete_task.active:
            delete_task.delete()
            return Response({'message':'task deleted successfully'})
        else:
            return Response({'message':'Task has been accepted, if you want to close this task, close this request from pending tab'})


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


#shows all live user tasks posted
class UserAllTaskView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = NewTask.objects.all()
    serializer_class = AllTaskSerializer

    def get_queryset(self):
        task_get = NewTask.objects.filter(user = self.request.user, active = True).order_by('-id')
        return task_get


#shows all live tasks for all users
class AllTaskView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    queryset = NewTask.objects.all()
    serializer_class = AllTaskSerializer

    def get_queryset(self):
        task_get = NewTask.objects.filter(active = True).order_by('-id')
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
            if not tasks.user == self.request.user:
                tasks.active = False
                assigned_object = UserAssigned.objects.create(user = tasks.user, delivery_user = self.request.user, task = tasks)
                pending_object = UserPending.objects.create(user = tasks.user, task = tasks, pending = True)

                assigned_object.save()
                pending_object.save()
                tasks.save(update_fields=['active'])
                return Response({'message':'Accepted this Request'})

            else:
                return Response({'message': 'You can not accept your own task....'})
        else:
            return Response({'This task has already been accepted..'})


#itempicked request
class ItemPickedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        
        accept_task_id = int(request.data['task_id'])
        tasks = NewTask.objects.get(pk = accept_task_id)
        picked = ItemPicked.objects.filter(task = tasks, picked = True).exists()

        if not picked:
            if not tasks.user == self.request.user:
                item_picked = ItemPicked.objects.create(user = tasks.user, task = tasks, picked = True)
                item_picked.save()
                return Response({'message':'Picked the item'})
            else:
                return Response({'message': 'You are not allowe to perform this action'})
        else:
            return Response({'Item has been picked already'})


#item_picked status
class ItemPickedStatusView(APIView):

    def post(self, request, *args, **kwargs):
        
        accept_task_id = int(request.data['task_id'])
        tasks = NewTask.objects.get(pk = accept_task_id)
        assigned = User.objects.get(user_delivery__task_id = accept_task_id)
        picked = ItemPicked.objects.filter(task = tasks, picked = True)
        picked_object = ItemPicked.objects.get(task = tasks)
        print(assigned)
        if picked.exists():
            return Response({'message':'your item has been picked up from the destination...','task':tasks.Title, 'task_location': tasks.location,'time_picked': picked_object.Time, 'delivery_user': assigned.first_name,
            'delivery_user_phone': assigned.phone}) #maybe something else like on your way...
        else:
            return Response({'message':'Item has not been picked'})

    

#accepted_Task_view for delivery_user
class PendingTaskUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = NewTask.objects.all()
    serializer_class = PendingTaskSerializer

    def get_queryset(self):
        delivery_user_tasks = NewTask.objects.filter(user_pending__pending = True)
        return (delivery_user_tasks)


#accepted_Task_view for self user delivering
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
        pending_user = UserAssigned.objects.get(task_id = accept_task_id)

        if not tasks.active:

            if assigned_task.pending:
                assigned_task.pending = False
                completed_object = UserCompleted.objects.create(user = tasks.user, task = tasks, completed = True)
                
                if User.objects.filter(user_delivery = pending_user.delivery_user.id).exists():
                    delivery_user = User.objects.get(user_delivery = pending_user.delivery_user.id)
                    delivery_user.user_status.deliveries_done += 1
                    delivery_user.user_status.save(update_fields = ['deliveries_done'])

                else:
                    delivery_user = User_status.objects.create(user = tasks.user, deliveries_done = 1)
                    delivery_user.save()
                    
                completed_object.save()
                self.request.user.completed_tasks += 1
                assigned_task.save(update_fields=['pending'])
                return Response({'message':'Task Completed successfully'})
                
            else:
                return Response({'message':'task is not pending anymore'})

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

