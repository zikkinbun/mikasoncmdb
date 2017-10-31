# coding: utf-8
from .models import Mysql_Monitor, Mysql_Replication, Mysql_Connection, Mysql_Status
from rest_framework import serializers

class MysqlMonitorSerializers(serializers.ModelSerializer):

    class Meta:
        model = Mysql_Monitor
        fields = '__all__'

class MysqlReplicationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Mysql_Replication
        fields = '__all__'

class MysqlStatusSerializers(serializers.ModelSerializer):

    class Meta:
        model = Mysql_Status
        fields = '__all__'

class MysqlConnSerializers(serializers.ModelSerializer):

    class Meta:
        model = Mysql_Connection
        fields = '__all__'
