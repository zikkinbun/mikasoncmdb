# coding: utf-8
from __future__ import unicode_literals
from django.db import models
import datetime
import time
# Create your models here.
class IDC(models.Model):
    Name = models.CharField(max_length=32, verbose_name=u'机房名称')
    LinkName = models.CharField(max_length=32, verbose_name=u'联系人')
    LinkPhone = models.CharField(max_length=32, verbose_name=u'联系电话')
    Network = models.TextField(blank=True, null=True, default='', verbose_name=u'IP地址')
    DateAdd = models.DateField(auto_now=True, null=True)
    Comment = models.CharField(max_length=128, blank=True, default='', null=True, verbose_name=u'备注')

    def __unicode__(self):
        return "{0}".format(self.Name)

class Server(models.Model):
    Name = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'主机名')
    System = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'系统平台')
    GlobalIpAddr = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'主机公网IP')
    PrivateIpAddr = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'主机私网IP')
    CpuStat = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'CPU')
    MemoryStat = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'内存')
    HDDStorage = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'硬盘')
    NetCard = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'网卡带宽')
    Status = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'是否在线')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'备注')
    CreateTime = models.DateTimeField(auto_now=True, null=True)

class Server_Service(models.Model):
    server_id = models.IntegerField()
    service_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'服务名称')
    service_status = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'服务状态')
    service_port = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'服务端口')
    service_version = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'服务版本')
    service_cmd = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'启动命令')

class Server_NetWorkStatus(models.Model):
    server_id = models.IntegerField()
    tcp_status = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'TCP状态')
    network_incoming = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'公网流入')
    network_outcoming = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'公网流出')

class Docker_Container(models.Model):
    hostName = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'主机名')
    containerId = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'容器ID')
    containerName = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'容器名')
    imageName = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'镜像名')
    command = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'启动命令')
    status = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'持续时间')
    state = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'容器状态')
    createdate = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'创建时间')

class Docker_Image(models.Model):
    imageId = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'镜像ID')
    imageName = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'镜像名')
    size = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'镜像大小')
    createdate = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'创建时间')
