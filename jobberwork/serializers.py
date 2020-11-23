from rest_framework import serializers
from .models import *
from users.models import User


class NewTaskSerializer(serializers.ModelSerializer):
    Time = serializers.TimeField(format="%H:%M", input_formats=['%H:%M'])
    class Meta:
        model = NewTask
        fields = (
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