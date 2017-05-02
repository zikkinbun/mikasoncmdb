# coding: utf-8
from django.db import models
from .models import cpuload, cpustat, memstat
from rest_framework import serializers

class cpuloadSerializers(serializers.ModelSerializer):

    class Meta:
        model = cpuload
        fields = '__all__'

class cpustatSerializers(serializers.ModelSerializer):

    class Meta:
        model = cpustat
        fields = '__all__'

class memstatSerializers(serializers.ModelSerializer):

    class Meta:
        model = memstat
        fields = '__all__'
