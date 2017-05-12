from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Task(models.Model):
    scriptId = models.IntegerField()
    executeTime = models.DateField(null=True, verbose_name=u'执行时间')
    targets = models.CharField(max_length=255, verbose_name=u'目标')
    timeout = models.DateField(null=True, verbose_name=u'超时')


class Script(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'脚本名称')
    path = models.CharField(null=True, max_length=255, verbose_name=u'脚本路径')
    origin = models.CharField(null=True, max_length=255, verbose_name=u'脚本来源')
    content = models.CharField(null=True, max_length=255, verbose_name=u'脚本内容')
    params = models.CharField(null=True, max_length=255, verbose_name=u'脚本参数')
    created = models.DateField(auto_now=True, null=True)
