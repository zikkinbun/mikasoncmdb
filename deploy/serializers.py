# coding: utf-8
from django.db import models
from .models import Projects, Records
from rest_framework import serializers

class ProjectsSerializers(serializers.ModelSerializer):

    # branches = serializers.SerializerMethodField()
    # tags = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = '__all__'

    # def get_branches(self, obj):
    #     return list(obj.branches)
    #
    # def get_tags(self, obj):
    #     return list(obj.tags)

class RecordsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Records
        fields = '__all__'
