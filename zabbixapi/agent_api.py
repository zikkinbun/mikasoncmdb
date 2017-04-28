# _*_ coding:utf-8_*_
import threading
import os
import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import *

def get_agent_cpu_data(request):
    if request.method == 'GET':
        hostlist = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.6', '192.168.1.7', '192.168.1.8', '192.168.1.9']
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

            system = os.popen(args1).read()
            user = os.popen(args2).read()
            idle = os.popen(args3).read()
            iowait = os.popen(args4).read()
            nice = os.popen(args5).read()
            softirq = os.popen(args6).read()
            steal = os.popen(args7).read()
            interrupt = os.popen(args8).read()

            cpustat.objects.create(system=system, user=user, idle=idle, iowait=iowait, nice=nice, \
                                softirq=softirq, steal=steal, interrupt=interrupt)
