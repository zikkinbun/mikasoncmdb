# coding: utf-8
from django.db import models
from rest_framework import serializers

from .models import Tcp_Status, Nginx_Status, Online_User, Network_Load

class TcpStatusSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tcp_Status
        fields = '__all__'

class NgStatusSerializers(serializers.ModelSerializer):

    class Meta:
        model = Nginx_Status
        fields = '__all__'

class OnlineUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = Online_User
        fields = '__all__'

class NetLoadSerializers(serializers.ModelSerializer):

    class Meta:
        model = Network_Load
        fields = '__all__'
