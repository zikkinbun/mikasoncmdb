#!/usr/bin/python
# coding: utf-8
from .models import Bussiness, BussinessData, BussinessTopu
from rest_framework import serializers

class BussinessSerializers(serializers.ModelSerializer):

    class Meta:
        model = Bussiness
        fields = '__all__'


class BussinessDataSerializers(serializers.ModelSerializer):

    class Meta:
        model = BussinessData
        fields = '__all__'


class BussinessTopuSerializers(serializers.ModelSerializer):

    class Meta:
        model = BussinessTopu
        fields = '__all__'
