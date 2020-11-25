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
            "active",
            "price",
        )

class AllTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "Time",
            "location",
            "active",
            "price",
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
            "active",
            "price",
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
    user_delivery = DeliveryUserSerializer(many = True, read_only = True)
    user_assigned = DeliveryUserSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = (
            "username",
            "phone",
            "user_delivery",
            "user_assigned"
        )

