# coding: utf-8
from django.db import models
from .models import Server, IDC, Docker_Container, Docker_Image
from rest_framework import serializers

class ServerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = '__all__'

class DockerContainerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Docker_Container
        fields = '__all__'

class DockerImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = Docker_Image
        fields = '__all__'
