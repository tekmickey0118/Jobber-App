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
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username
    class Meta:
        model = NewTask
        fields = (
            "id",
            "user",
            "Title",
            "Time",
            "location",
            "active",
            "price",
        )


class IndividualTaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username,obj.user.phone,obj.user.hostel_room
    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "user",
            "Description",
            "Time",
            "Date",
            "location",
            "active",
            "price",
        )


class UserIndividualTaskSerializer(serializers.ModelSerializer):
    user_assigned = IndividualTaskSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = (
            "username",
            "phone",
            "user_delivery",
            "user_assigned"
        )


class DeliveryUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    delivery_user = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username,obj.user.phone

    def get_delivery_user(self, obj):
        return obj.delivery_user.username, obj.delivery_user.phone

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


class PendingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = UserPending
        fields = (
            "id",
            "user",
            "task",
            'pending',
        )

class PendingTaskSerializer(serializers.ModelSerializer):
    user_pending = PendingSerializer(read_only = True)

    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "price",
            "user_pending"
        )


class CompletedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = UserCompleted
        fields = (
            "id",
            "user",
            "task",
            'completed',
        )


class CompletedTaskSerializer(serializers.ModelSerializer):
    user_completed = CompletedSerializer(read_only = True)

    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "price",
            "user_completed"
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

