#!/usr/bin/python
# coding: utf-8
from __future__ import absolute_import, unicode_literals
from django.conf import settings
import os
import time

from datetime import datetime
from celery import Celery



# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deploySystem.settings')

app = Celery('deploySystem')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(name='periods.deploy_task.deployTask')
def deployTask():
    from deploy.models import PeriodTask
    from deploy.serializers import PeriodTaskSerializers
    from deploy.internal_deploy_api import PeriodDeploy

    try:
        datas = PeriodTask.objects.all()
        serializer = PeriodTaskSerializers(datas, many=True)
        for task in serializer.data:
            if task['status'] == 0:
                current_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
                # print type(current_time)
                # print type(task['period'])
                # time_range = current_time - task['period']
                # print time_ranger
                if str(task['period']) == current_time:
                    periodtask = PeriodDeploy(task['project'], task['branch'], task['tag'], task['config'], task['type'], task['env'], task['target'])
                    status = periodtask.run()
                    if status['retcode'] == 0:
                        PeriodTask.objects.filter(id=task['id']).update(status=1)
                    else:
                        PeriodTask.objects.filter(id=task['id']).update(status=2)
                else:
                    print 'the time is not match'
            else:
                print 'the task is already excuted'
    except Exception as e:
        print e

@app.task(name='periods.zabbix_agent_task.get_agent_cpu_data')
def get_agent_cpu_data():
    from zabbixapi.models import cpustat

    hostlist = ['192.168.1.209', '127.0.0.1', '192.168.1.211', '192.168.1.212', '192.168.1.213', '192.168.1.214', '192.168.1.215']
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
                            softirq=softirq, steal=steal, interrupt=interrupt, created=datetime.now())

@app.task(name='periods.zabbix_agent_task.get_agent_cpu_load')
def get_agent_cpu_load():
    from zabbixapi.models import cpuload

    hostlist = ['192.168.1.209', '127.0.0.1', '192.168.1.211', '192.168.1.212', '192.168.1.213', '192.168.1.214', '192.168.1.215']
    os.chdir('/usr/local/zabbix/bin')
    for host in hostlist:
        args1 = './zabbix_get -s %s -p 10050 -k "system.cpu.load[all,avg1]"' % host
        args2 = './zabbix_get -s %s -p 10050 -k "system.cpu.load[all,avg5]"' % host
        args3 = './zabbix_get -s %s -p 10050 -k "system.cpu.load[all,avg15]"' % host

        avg1 = os.popen(args1).read().strip()
        avg5 = os.popen(args2).read().strip()
        avg15 = os.popen(args3).read().strip()

        cpuload.objects.create(hostip=host, avg1=avg1, avg5=avg5, avg15=avg15, created=datetime.now())

@app.task(name='periods.zabbix_agent_task.get_agent_mem_stat')
def get_agent_mem_stat():
    from zabbixapi.models import memstat

    hostlist = ['192.168.1.209', '127.0.0.1', '192.168.1.211', '192.168.1.212', '192.168.1.213', '192.168.1.214', '192.168.1.215']
    os.chdir('/usr/local/zabbix/bin')
    for host in hostlist:
        args1 = './zabbix_get -s %s -p 10050 -k "vm.memory.size[available]"' % host
        args2 = './zabbix_get -s %s -p 10050 -k "vm.memory.size[total]"' % host

        available = os.popen(args1).read().strip()
        total = os.popen(args2).read().strip()

        memstat.objects.create(hostip=host, available=available, total=total, created=datetime.now())

@app.task(name='periods.zabbix_agent_task.agent_ping')
def agent_ping():
    from asset.models import Server

    itemlist = ['23682', '23804', '23870', '23911', '23952', '23993', '23287']
    namelist = ['uco2_dev', 'uco2_test', 'uco2_rd_prod', 'uco2_sql_mt', 'uco2_sql_sl', 'uco2_web_prod', 'uco2_oper']
    idlist = [9, 2, 3, 4, 5, 6, 7]
    method = "history.get"
    data = {}
    for i in range(len(itemlist)):
        params = {
                "output": "extend",
                "history": 3,
                "itemids": itemlist[i],
                "limit": 10
                }
        origin = processData(method, params)
        for host in origin:
            ping = int(host[u'value'])
            data[namelist[i]] = ping
    servers = Server.objects.all()
    for server in servers:
        ping = data[server[name]]
            # print type(ping)
        if ping == 1:
            Server.objects.filter(name=server[name]).update(status='在线')
        else:
            Server.objects.filter(name=server[name]).update(status='不在线')
    return "{'data': '请求成功'}"


@app.task(name='dbmonitor.task.get_replication')
def get_replication():
    from dbmonitor.models import Mysql_Monitor
    from dbmonitor.serializers import MysqlMonitorSerializers
    from dbmonitor.mysql_library import repl_update_or_create
    from dbmonitor.connector import mysql_connector

    infos = Mysql_Monitor.objects.all()
    serializer = MysqlMonitorSerializers(infos, many=True)
    sql = 'show slave status'
    if serializer.data:
        for info in serializer.data:
            if info['check_slave'] == 1 or info['check_slave'] == '1':
                cursor = mysql_connector(info['db_ip'], info['db_port'], info['db_user'], info['db_pass'])
                data = cursor.select_all(sql)
                record = repl_update_or_create(data, info['db_ip'], info['db_port'])
            else:
                continue

@app.task(name='dbmonitor.task.get_global_status')
def get_global_status():
    from dbmonitor.models import Mysql_Monitor
    from dbmonitor.serializers import MysqlMonitorSerializers
    from dbmonitor.mysql_library import status_create, status_querySet
    from dbmonitor.connector import mysql_connector

    infos = Mysql_Monitor.objects.all()
    serializer = MysqlMonitorSerializers(infos, many=True)
    sql = "show global status"
    if serializer.data:
        for info in serializer.data:
            if info['check_status'] == 1 or info['check_status'] == '1':
                # print info['check_status']
                cursor = mysql_connector(info['db_ip'], info['db_port'], info['db_user'], info['db_pass'])
                datas = cursor.select_all(sql)
                # print datas
                status_dataset = status_querySet(datas)
                # print status_dataset
                record = status_create(status_dataset, info['db_ip'], info['db_port'])
            else:
                continue

@app.task(name='dbmonitor.task.get_connections')
def get_connections():
    from dbmonitor.models import Mysql_Monitor
    from dbmonitor.serializers import MysqlMonitorSerializers
    from dbmonitor.mysql_library import connection_querySet, connection_update_or_create, connection_create
    from dbmonitor.connector import mysql_connector

    sql = "show status like '%connect%'"
    infos = Mysql_Monitor.objects.all()
    # print infos
    serializer = MysqlMonitorSerializers(infos, many=True)
    if serializer.data:
        for info in serializer.data:
            # print info
            if info['check_connections'] == 1 or info['check_connections'] == '1':
                cursor = mysql_connector(info['db_ip'], info['db_port'], info['db_user'], info['db_pass'])
                datas = cursor.select_all(sql)
                dataset = connection_querySet(datas)
                record = connection_create(dataset, info['db_ip'], info['db_port'])
            else:
                continue
