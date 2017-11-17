# coding: utf-8
from django.db import models
from .models import Records, PeriodTask
from rest_framework import serializers

class RecordsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Records
        fields = '__all__'

class PeriodTaskSerializers(serializers.ModelSerializer):

    class Meta:
        model = PeriodTask
        fields = '__all__'
