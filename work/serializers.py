# coding: utf-8
from django.db import models
from rest_framework import serializers

from .models import Task, Script

class TaskSerializers(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class ScriptSerializers(serializers.ModelSerializer):

    class Meta:
        models = Script
        fields = '__all__'
