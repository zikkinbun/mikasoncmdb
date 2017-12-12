# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import utc

from datetime import datetime

# Create your models here.

class Bussiness(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    projectid = models.IntegerField(db_column='projectId', blank=True, null=True)  # Field name made lowercase.
    operatorid = models.IntegerField(db_column='operatorId', blank=True, null=True)  # Field name made lowercase.
    productorid = models.IntegerField(db_column='productorId', blank=True, null=True)  # Field name made lowercase.
    hostnum = models.IntegerField(db_column='hostNum', blank=True, null=True)  # Field name made lowercase.
    creator = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'bussiness'


class BussinessData(models.Model):
    bussinessid = models.IntegerField(db_column='bussinessId', blank=True, null=True)  # Field name made lowercase.
    serverid = models.CharField(db_column='serverId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    system_status = models.IntegerField(blank=True, null=True)
    firewall = models.IntegerField(blank=True, null=True)
    host_info = models.CharField(max_length=255, blank=True, null=True)
    router_info = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'bussiness_data'


class BussinessTopu(models.Model):
    bussinessid = models.IntegerField(db_column='bussinessId', blank=True, null=True)  # Field name made lowercase.
    serverid = models.IntegerField(db_column='serverId', blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='moduleId', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'bussiness_topu'
