from __future__ import unicode_literals

from django.db import models

# Create your models here.

class cpustat(models.Model):
    hostip = models.CharField(max_length=32)
    system = models.CharField(max_length=32)
    user = models.CharField(max_length=32)
    idle = models.CharField(max_length=32)
    iowait = models.CharField(max_length=32)
    nice = models.CharField(max_length=32)
    softirq = models.CharField(max_length=32)
    steal = models.CharField(max_length=32)
    interrupt = models.CharField(max_length=32)
    created = models.DateField(auto_now=True, null=True)

class cpuload(models.Model):
    hostip = models.CharField(max_length=32)
    avg1 = models.CharField(max_length=32)
    avg5 = models.CharField(max_length=32)
    avg15 = models.CharField(max_length=32)

class memstat(models.Model):
    hostip = models.CharField(max_length=32)
    available = models.CharField(max_length=32)
    total = models.CharField(max_length=32)
    created = models.DateField(auto_now=True, null=True)
