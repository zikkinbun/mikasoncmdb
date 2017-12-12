# coding: utf-8
from .models import MonitorMysqlConnection, MonitorMysqlProcesslist, MonitorMysqlReplication, MonitorMysqlStatus, MonitorMysqlSlowQueryHis, MonitorCpuLoad, MonitorHddStat, MonitorMemStat, MonitorFunction, MonitorNetworkLoad, MonitorNginxStatus, MonitorOnlineUser, MonitorTcpStatus, MonitorMysqlUser

from rest_framework import serializers

class MysqlSlowQueryHisSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorMysqlSlowQueryHis
        fields = '__all__'

class MysqlReplicationSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorMysqlReplication
        fields = '__all__'

class MysqlStatusSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorMysqlStatus
        fields = '__all__'

class MysqlConnSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorMysqlConnection
        fields = '__all__'

class MysqlProcSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorMysqlProcesslist
        fields = '__all__'

class CpuLoadSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorCpuLoad
        fields = '__all__'

class HddStatSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorHddStat
        fields = '__all__'

class MemStatSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorMemStat
        fields = '__all__'

class MonitorFunctionSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorFunction
        fields = '__all__'

class MonitorMysqlUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = MonitorMysqlUser
        fields = '__all__'
