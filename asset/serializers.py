# coding: utf-8
from django.db import models
from .models import Server, IDC
from rest_framework import serializers

# class ServerSerializers(serializers.Serializer):
#
#     Name = serializers.CharField(max_length=32)
#     System = serializers.CharField(max_length=128)
#     GlobalIpAddr = serializers.CharField(max_length=255)
#     PrivateIpAddr = serializers.CharField(max_length=255)
#     CpuStat = serializers.CharField(max_length=32)
#     MemoryStat = serializers.CharField(max_length=32)
#     HDDStorage = serializers.CharField(max_length=32)
#     NetCard = serializers.CharField(max_length=32)
#     Status = serializers.CharField(max_length=20)
#     comment = serializers.CharField(max_length=255)
#     CreateTime = serializers.DateTimeField()
#
#     # metion 1
#     def create(self, validated_data):
#         """
#             响应POST请求
#         """
#         return Server(**validated_data)
#
#     def update(self, instance, validated_data):
#         if instance:
#             instance.Name = validated_data.get('Name', instance.Name)
#             instance.System = validated_data.get('System', instance.System)
#             instance.GlobalIpAddr = validated_data.get('GlobalIpAddr', instance.GlobalIpAddr)
#             instance.PrivateIpAddr = validated_data.get('PrivateIpAddr', instance.PrivateIpAddr)
#             instance.CpuStat = validated_data.get('CpuStat', instance.CpuStat)
#             instance.MemoryStat = validated_data.get('MemoryStat', instance.MemoryStat)
#             instance.HDDStorage = validated_data.get('HDDStorage', instance.HDDStorage)
#             instance.NetCard = validated_data.get('NetCard', instance.NetCard)
#             instance.Status = validated_data.get('Status', instance.Status)
#             instance.comment = validated_data.get('comment', instance.comment)
#             instance.save()
#             return instance

class ServerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = '__all__'
