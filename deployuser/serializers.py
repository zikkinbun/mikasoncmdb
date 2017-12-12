# coding: utf-8
from django.db import models
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
