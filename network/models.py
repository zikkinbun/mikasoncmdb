# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.timezone import utc
from datetime import datetime

# Create your models here.

class Network_Monitor(models.Model):
    server_id = models.IntegerField(blank=True, null=True)
    check_tcp = models.IntegerField(default=0)
    check_ng = models.IntegerField(default=0)
    check_tty = models.IntegerField(default=0)
    check_netload = models.IntegerField(default=0)
    check_proc = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

class Tcp_Status(models.Model):
    server_id = models.IntegerField(blank=True, null=True)
    listen = models.IntegerField(blank=True, null=True)
    established = models.IntegerField(blank=True, null=True)
    time_wait = models.IntegerField(blank=True, null=True)
    close_wait = models.IntegerField(blank=True, null=True)
    closed = models.IntegerField(blank=True, null=True)
    syn_sent = models.IntegerField(blank=True, null=True)
    syn_received = models.IntegerField(blank=True, null=True)
    last_ack = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

class Nginx_Status(models.Model):
    server_id = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    reading = models.IntegerField(blank=True, null=True)
    writing = models.IntegerField(blank=True, null=True)
    waiting = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

class Online_User(models.Model):
    server_id = models.IntegerField(blank=True, null=True)
    user_name = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=32, blank=True, null=True)
    chn = models.CharField(max_length=32, blank=True, null=True)
    uptime = models.CharField(max_length=32, blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

class Network_Load(models.Model):
    server_id = models.IntegerField(blank=True, null=True)
    private_incoming = models.FloatField(blank=True, null=True)
    private_outgoing = models.FloatField(blank=True, null=True)
    global_incoming = models.FloatField(blank=True, null=True)
    global_outgoing = models.FloatField(blank=True, null=True)
    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))
