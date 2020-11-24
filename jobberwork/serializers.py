from rest_framework import serializers
from .models import *
from users.models import User
from drf_writable_nested import WritableNestedModelSerializer

class NewTaskSerializer(serializers.ModelSerializer):
    Time = serializers.TimeField(format="%H:%M", input_formats=['%H:%M'])
    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "Description",
            "Time",
            "Date",
            "location",
            "active"
        )

class AllTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "Time",
            "location",
            "active"
        )


class IndividualTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "Description",
            "Time",
            "Date",
            "location",
            "active"
        )

class DeleteTaskSerializer(serializers.ModelSerializer):
    Time = serializers.TimeField(format="%H:%M", input_formats=['%H:%M'])
    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "Description",
            "Time",
            "Date",
            "location",
            "active"
        )


class CompletedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompleted
        fields = (
            "completed"
        )

class DeliveryUserAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAssigned
        fields = (
            "user",
            "delivery_user",
            "task",
        )

class UserDeliveryUserAcceptSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    user_assigned = DeliveryUserAcceptSerializer()
    class Meta:
        model = NewTask
        fields = (
            "user",
            "user_assigned",
        )


class DeliveryUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    delivery_user = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_delivery_user(self, obj):
        return obj.delivery_user.username

    def get_task(self, obj):
        return obj.task.Title

    class Meta:
        model = UserAssigned
        fields = (
            "id",
            "user",
            "delivery_user",
            "task"
        )


class UserSerializer(serializers.ModelSerializer):
    user_delivery = DeliveryUserSerializer(read_only = True)
    user_assigned = DeliveryUserSerializer(read_only = True)

    class Meta:
        model = User
        fields = (
            "username",
            "phone",
            "user_delivery",
            "user_assigned"
        )

class UserAcceptSerializer(serializers.ModelSerializer):
    user_delivery = DeliveryUserSerializer(read_only = True)
    user_assigned = DeliveryUserSerializer(read_only = True, source = 'delivery_user.username')

    class Meta:
        model = User
        fields = (
            "username",
            "user_delivery",
            "user_assigned"
        )
