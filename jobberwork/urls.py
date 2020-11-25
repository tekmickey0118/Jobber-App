from django.urls import path
from .views import *

urlpatterns = [
    path('task/new/', NewTaskView.as_view()),

    path('task/all/', AllTaskView.as_view()),
    path('task/all/me/', UserAllTaskView.as_view()),
    path('task/me/<int:id>/', UserIndividualTaskView.as_view()),
    path('task/<int:id>/', IndividualTaskView.as_view()),
    path('task/edit/<int:id>/', UserEditIndividualTaskView.as_view()),

    path('task/accept/', AcceptedTaskView.as_view()),
    path('task/accept/delivery', PendingTaskUserView.as_view()),
    path('task/accept/delivery/me', MyAcceptedTaskView.as_view()),

    path('task/complete/', CompletedTaskView.as_view()),
    path('task/complete/all', CompletedTaskUserView.as_view()),

    path('task/cancel/', CancelTaskView.as_view()),
    path('task/cancel/all', UncompletedTaskUserView.as_view()),


]