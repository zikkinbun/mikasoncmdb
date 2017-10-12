#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class Records(models.Model):
    project_name = models.CharField(max_length=50, verbose_name=u'发布项目名')
    project_owner = models.CharField(max_length=32, verbose_name=u'项目负责人')
    project_type = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'项目类型')
    project_env = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'项目环境')
    deploy_branch = models.CharField(max_length=32, verbose_name=u'发布分支')
    deploy_tag = models.CharField(max_length=32, verbose_name=u'发布标签')
    deploy_status = models.CharField(max_length=32, verbose_name=u'发布状态')
    comment = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'备注')
    deploy_time = models.DateField(blank=True, default=datetime.now)

class Projects(models.Model):
    pid = models.IntegerField(max_length=32, verbose_name=u'项目ID')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'项目名称')
    type = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'项目类型')
    ssh_url = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'项目SSH地址')
    http_url = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'项目HTTP地址')
    branches = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'项目分支')
    tags = models.TextField(max_length=1000, blank=True, null=True, verbose_name=u'项目标签')
    configfile = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'项目配置')
    owner = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'项目负责人')
    createdate = models.DateField(blank=True, default=datetime.now)

        
