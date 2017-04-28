# _*_ coding:utf-8_*_
import os
import json
from celery import task

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import *

@task
def get_agent_cpu_data():
    hostlist = ['192.168.1.1', '127.0.0.1', '192.168.1.3', '192.168.1.6', '192.168.1.7', '192.168.1.8', '192.168.1.9']
    os.chdir('/usr/local/zabbix/bin')
    for host in hostlist:
        args1 = './zabbix_get -s %s -p 10050 -k "system.cpu.util[,system]"' % host
        args2 = './zabbix_get -s %s -p 10050 -k "system.cpu.util[,user]"' % host
        args3 = './zabbix_get -s %s -p 10050 -k "system.cpu.util[,idle]"' % host
        args4 = './zabbix_get -s %s -p 10050 -k "system.cpu.util[,iowait]"' % host
        args5 = './zabbix_get -s %s -p 10050 -k "system.cpu.util[,nice]"' % host
        args6 = './zabbix_get -s %s -p 10050 -k "system.cpu.util[,softirq]"' % host
        args7 = './zabbix_get -s %s -p 10050 -k "system.cpu.util[,steal]"' % host
        args8 = './zabbix_get -s %s -p 10050 -k "system.cpu.util[,interrupt]"' % host

        system = os.popen(args1).read().strip()
        user = os.popen(args2).read().strip()
        idle = os.popen(args3).read().strip()
        iowait = os.popen(args4).read().strip()
        nice = os.popen(args5).read().strip()
        softirq = os.popen(args6).read().strip()
        steal = os.popen(args7).read().strip()
        interrupt = os.popen(args8).read().strip()

        cpustat.objects.create(hostip=host, system=system, user=user, idle=idle, iowait=iowait, nice=nice, \
                            softirq=softirq, steal=steal, interrupt=interrupt)

@task
def get_agent_cpu_load():
    hostlist = ['192.168.1.1', '127.0.0.1', '192.168.1.3', '192.168.1.6', '192.168.1.7', '192.168.1.8', '192.168.1.9']
    os.chdir('/usr/local/zabbix/bin')
    for host in hostlist:
        args1 = './zabbix_get -s %s -p 10050 -k "system.cpu.load[all,avg1]"' % host
        args2 = './zabbix_get -s %s -p 10050 -k "system.cpu.load[all,avg5]"' % host
        args3 = './zabbix_get -s %s -p 10050 -k "system.cpu.load[all,avg15]"' % host

        avg1 = os.popen(args1).read().strip()
        avg5 = os.popen(args2).read().strip()
        avg15 = os.popen(args3).read().strip()

        cpuload.objects.create(hostip=host, avg1=avg1, avg5=avg5, avg15=avg15)

@task
def get_agent_mem_stat():
    hostlist = ['192.168.1.1', '127.0.0.1', '192.168.1.3', '192.168.1.6', '192.168.1.7', '192.168.1.8', '192.168.1.9']
    os.chdir('/usr/local/zabbix/bin')
    for host in hostlist:
        args1 = './zabbix_get -s %s -p 10050 -k "vm.memory.size[available]"' % host
        args2 = './zabbix_get -s %s -p 10050 -k "vm.memory.size[total]"' % host

        available = os.popen(args1).read().strip()
        total = os.popen(args2).read().strip()

        memstat.objects.create(hostip=host, available=available, avgtotal5=total)
