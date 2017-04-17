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

    # CPU = (
    #     ('16Core', '16'),
    #     ('8Core','8'),
    #     ('4Core', '4'),
    #     ('2Core', '2')
    # )
    #
    # MEM = (
    #     ('32G', '32'),
    #     ('16G', '16'),
    #     ('8G', '8'),
    #     ('4G', '4')
    # )
    #
    # STATUS = (
    #     ('Online', 'ON'),
    #     ('Offline', 'OFF')
    # )

    Name = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'主机名')
    System = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'系统平台')
    GlobalIpAddr = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'主机公网IP')
    PrivateIpAddr = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'主机私网IP')
    # CpuStat = models.CharField(max_length=32, choices=CPU, verbose_name=u'CPU')
    # MemoryStat = models.CharField(max_length=32, choices=MEM, verbose_name=u'内存')
    CpuStat = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'CPU')
    MemoryStat = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'内存')
    HDDStorage = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'硬盘')
    NetCard = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'网卡带宽')
    # Status = models.CharField(max_length=20, choices=STATUS, verbose_name=u'是否激活')
    Status = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'是否在线')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'备注')
    CreateTime = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.Name

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}".format(self.Name, \
                                                                                       self.System, self.GlobalIpAddr, self.CpuStat, \
                                                                                       self.MemoryStat, self.HDDStorage, self.NetCard, \
                                                                                       self.Status, self.CreateTime, self.comment)

class Server_Status(models.Model):
    server_id = models.IntegerField()
    login_user = models.CharField(max_length=10, blank=True, null=True, verbose_name=u'用户登录数')
