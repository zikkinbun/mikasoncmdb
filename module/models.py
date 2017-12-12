# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import utc

from datetime import datetime

# Create your models here.

class Module(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'module'


class ModuleDetail(models.Model):
    port = models.CharField(max_length=255, blank=True, null=True)
    moduleid = models.CharField(db_column='moduleId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serverid = models.CharField(db_column='serverId', max_length=255, blank=True, null=True)
    is_actived = models.IntegerField(default=0)
    configfile = models.TextField(blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'module_detail'


class ModuleServerRelate(models.Model):
    serverid = models.IntegerField(db_column='serverId', blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='moduleId', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'module_server_relate'
