# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Job(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    is_exec = models.IntegerField(blank=True, null=True)
    exectime = models.DateTimeField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job'


class JobCrond(models.Model):
    jobid = models.IntegerField(db_column='jobId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)
    param = models.CharField(max_length=255, blank=True, null=True)
    exectime = models.DateTimeField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_crond'


class JobExecute(models.Model):
    jobid = models.IntegerField(db_column='jobId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.IntegerField(blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    param = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_execute'


class JobNormal(models.Model):
    jobid = models.IntegerField(db_column='jobId', blank=True, null=True)  # Field name made lowercase.
    creator = models.IntegerField(blank=True, null=True)
    updatetime = models.DateTimeField(blank=True, null=True)
    lasttime = models.DateTimeField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_normal'


class JobUpload(models.Model):
    jobid = models.IntegerField(db_column='jobId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    filepath = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    filetype = models.IntegerField(blank=True, null=True)
    createdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_upload'
