# _*_ coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Task(models.Model):
    scriptId = models.IntegerField()
    executeTime = models.DateField(null=True, verbose_name=u'执行时间')
    targets = models.CharField(max_length=255, verbose_name=u'目标')
    timeout = models.DateField(null=True, verbose_name=u'超时')

class ManualScript(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'脚本名称')
    content = models.CharField(null=True, max_length=255, verbose_name=u'脚本内容')
    params = models.CharField(null=True, max_length=255, verbose_name=u'脚本参数')
    path = models.FileField(verbose_name=u'创建路径')
    created = models.DateField(auto_now=True, null=True)

class UploadScript(models.Model):
    name = models.CharField(null=True, max_length=255, verbose_name=u'脚本名称')
    params = models.CharField(null=True, max_length=255, verbose_name=u'脚本参数')
    path = models.FileField(upload_to='../files/', verbose_name=u'上传路径')
    created = models.DateField(auto_now=True, null=True)

class ServerUser(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'用户名')
    roler = models.CharField(max_length=32, verbose_name=u'权限角色')
    uid = models.IntegerField()
    gid = models.IntegerField()
    comment = models.CharField(null=True, max_length=255, verbose_name=u'备注')
