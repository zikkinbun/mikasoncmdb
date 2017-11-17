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

class PeriodTask(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'任务名称')
    project = models.CharField(max_length=50, verbose_name=u'项目名称')
    branch = models.CharField(max_length=32, verbose_name=u'分支')
    tag = models.CharField(max_length=32, verbose_name=u'标签')
    env = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'任务环境')
    config = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'配置文件')
    type = models.CharField(max_length=32, verbose_name=u'项目类型')
    period = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'定时器')
    status = models.IntegerField(verbose_name=u'状态')
    target = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'目标')
    createdate = models.DateField(blank=True, default=datetime.now())
