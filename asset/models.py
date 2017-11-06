# coding: utf-8
from __future__ import unicode_literals
from django.db import models
import datetime
import time
# Create your models here.

class Server(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'主机名')
    system = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'系统平台')
    glabal_ip = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'主机公网IP')
    private_ip = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'主机私网IP')
    cpu_status = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'CPU')
    mem_status = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'内存')
    hdd_storage = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'硬盘')
    net_flow = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'网卡带宽')
    status = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'是否在线')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'备注')
    salt_alias = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'salt别名')
    create_time = models.DateTimeField(auto_now=True, null=True)

class Server_Service(models.Model):
    server_id = models.IntegerField()
    service_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'服务名称')
    service_status = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'服务状态')
    service_port = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'服务端口')
    service_version = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'服务版本')
    service_cmd = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'启动命令')

class Docker_Container(models.Model):
    host_name = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'主机名')
    container_id = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'容器ID')
    container_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'容器名')
    image_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'镜像名')
    command = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'启动命令')
    status = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'持续时间')
    state = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'容器状态')
    create_date = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'创建时间')

class Docker_Image(models.Model):
    image_id = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'镜像ID')
    image_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'镜像名')
    size = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'镜像大小')
    create_date = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'创建时间')
