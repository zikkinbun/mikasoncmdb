from __future__ import unicode_literals

from django.db import models

# Create your models here.

class cpustat(models.Model):
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
    avg1 = models.CharField(max_length=32)
    avg5 = models.CharField(max_length=32)
    avg15 = models.CharField(max_length=32)

class memstat(models.Model):
    available = models.CharField(max_length=32)
    total = models.CharField(max_length=32)
    created = models.DateField(auto_now=True, null=True)
