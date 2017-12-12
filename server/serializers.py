# coding: utf-8
from django.db import models
from .models import Server, ServerContainer, ServerImage, ServerDetail, \
    ServerMonitorFuncRelation, ServerProjects, ServerClusterRelate, Cluster
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

class ClusterSerializers(serializers.ModelSerializer):

    class Meta:
        model = Cluster
        fields = '__all__'

class ServerClusterRelateSerializers(serializers.ModelSerializer):

    class Meta:
        model = ServerClusterRelate
        fields = '__all__'
