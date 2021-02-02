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
            "to_location",
            "active",
            "price",
        )

class AllTaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.first_name, obj.user.profile_pic.url
    class Meta:
        model = NewTask
        fields = (
            "id",
            "user",
            "Title",
            "Time",
            "location",
            "to_location",
            "active",
            "price",
        )

class IndividualTaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.first_name,obj.user.reg_number, obj.user.profile_pic.url
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
            "to_location",
            "active",
            "price",
        )


class UserIndividualTaskSerializer(serializers.ModelSerializer):
    user_assigned = IndividualTaskSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "phone",
            "user_delivery",
            "user_assigned"
        )


class DeliveryUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    delivery_user = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.first_name,obj.user.phone, obj.user.profile_pic.url

    def get_delivery_user(self, obj):
        return obj.delivery_user.first_name, obj.delivery_user.phone, obj.delivery_user.profile_pic.url

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


class IndividualAcceptTaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_assigned = DeliveryUserSerializer(read_only = True)


    def get_user(self, obj):
        return obj.user.first_name,obj.user.phone,obj.user.hostel_room,obj.user.reg_number, obj.user.profile_pic.url

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
            "to_location",
            "active",
            "price",
            "user_assigned",
        )



class PendingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.first_name

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
        return obj.user.first_name, obj.user.profile_pic

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
    user_delivery = DeliveryUserSerializer(many = True, read_only = True)
    user_assigned = DeliveryUserSerializer(many = True, read_only = True)

    class Meta:
        model = NewTask
        fields = (
            "id",
            "Title",
            "price",
            "user_completed",
            "user_delivery",
            "user_assgigned"
        )


class UserSerializer(serializers.ModelSerializer):
    user_delivery = DeliveryUserSerializer(many = True, read_only = True)
    user_assigned = DeliveryUserSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "phone",
            "user_delivery",
            "user_assigned"
        )

