# coding: utf-8
from django.db import models
from .models import Server, ServerContainer, ServerImage, ServerDetail, \
    ServerMonitorFuncRelation, ServerProjects, ServerSevice
from rest_framework import serializers

class ServerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = '__all__'

class ServerContainerSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServerContainer
        fields = '__all__'

class ServerImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServerImage
        fields = '__all__'

class ServerDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServerDetail
        fields = '__all__'


class ServerMonitorFuncRelationSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServerMonitorFuncRelation
        fields = '__all__'

class ServerProjectsSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServerProjects
        fields = '__all__'

class ServerSeviceSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServerSevice
        fields = '__all__'
