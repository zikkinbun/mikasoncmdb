#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class deployRecord(models.Model):
    project_name = models.CharField(max_length=50, verbose_name=u'发布项目名')
    project_owner = models.CharField(max_length=32, verbose_name=u'项目负责人')
    deploy_branch = models.CharField(max_length=32, verbose_name=u'发布分支')
    deploy_tag = models.CharField(max_length=32, verbose_name=u'发布标签')
    deploy_time = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}".format(self.project_name, self.project_owner, \
                                                    self.deploy_branch, self.deploy_tag, \
                                                    self.deploy_time)

    def __unicode__(self):
        return self.project_name
