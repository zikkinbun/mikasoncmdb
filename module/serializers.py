#!/usr/bin/python
# coding: utf-8
from .models import Module, ModuleDetail, ModuleServerRelate
from rest_framework import serializers

class ModuleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = '__all__'


class ModuleDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = ModuleDetail
        fields = '__all__'


class ModuleServerRelateSerializers(serializers.ModelSerializer):

    class Meta:
        model = ModuleServerRelate
        fields = '__all__'
