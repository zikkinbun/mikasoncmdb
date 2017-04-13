# coding: utf-8
from django.db import models
from .models import Server, IDC
from rest_framework import serializers

class ServerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = '__all__'
