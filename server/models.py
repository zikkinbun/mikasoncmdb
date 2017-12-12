# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import utc

from datetime import datetime
# Create your models here.

class Server(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    alias = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=0)
    is_monitor = models.IntegerField(default=0)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'server'


class ServerContainer(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    container_id = models.CharField(max_length=255, blank=True, null=True)
    container_name = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    command = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'server_container'


class ServerDetail(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    cpu = models.CharField(max_length=255, blank=True, null=True)
    mem = models.CharField(max_length=255, blank=True, null=True)
    netflow = models.CharField(max_length=255, blank=True, null=True)
    hdd = models.CharField(max_length=255, blank=True, null=True)
    system = models.CharField(max_length=255, blank=True, null=True)
    core = models.CharField(max_length=255, blank=True, null=True)
    global_ip = models.CharField(max_length=255, blank=True, null=True)
    private_ip = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'server_detail'


class ServerImage(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    image_id = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=32, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'server_image'


class ServerMonitorFuncRelation(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    funcId = models.IntegerField(blank=True, null=True)
    is_actived = models.IntegerField(default=0)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'server_monitor_func_relation'


class ServerProjects(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=32, blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True)
    ssh_url = models.CharField(max_length=255, blank=True, null=True)
    http_url = models.CharField(max_length=255, blank=True, null=True)
    branches = models.CharField(max_length=255, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    configfile = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=32, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'project'


class ServerUser(models.Model):
    serverid = models.IntegerField(db_column='serverId', blank=True, null=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='groupId', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    creatdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'server_user'


class Cluster(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'cluster'


class ServerClusterRelate(models.Model):
    serverid = models.IntegerField(db_column='serverId', blank=True, null=True)
    clusterid = models.IntegerField(db_column='clusterId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'server_cluster_relate'
