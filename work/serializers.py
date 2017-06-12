# coding: utf-8
from django.db import models
from rest_framework import serializers

from .models import Task, ManualScript, UploadScript, ServerUser

class TaskSerializers(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class ManualScriptSerializers(serializers.ModelSerializer):

    class Meta:
        model = ManualScript
        fields = '__all__'

class UploadScriptSerializers(serializers.ModelSerializer):

    class Meta:
        model = UploadScript
        fields = '__all__'

class ServerUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServerUser
        fields = '__all__'
