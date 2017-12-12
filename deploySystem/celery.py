#!/usr/bin/python
# coding: utf-8
from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.db import connection
import os
import time
import inspect
import logging

from datetime import datetime
from celery import Celery

logger = logging.getLogger('sourceDns.webdns.views')

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


@app.task(name='monitor.task.get_agent_cpu_data')
def get_agent_cpu_data():
    pass


@app.task(name='monitor.task.get_agent_cpu_load')
def get_agent_cpu_load():
    pass


@app.task(name='monitor.task.get_agent_mem_stat')
def get_agent_mem_stat():
    pass


@app.task(name='monitor.task.agent_ping')
def agent_ping():
    pass


@app.task(name='monitor.task.get_replication')
def get_replication():
    from monitor.mysql_library import repl_update_or_create
    from monitor.connector import mysql_connector

    sql = 'show slave status'
    try:
        with connection.cursor() as cursor:
            query = 'SELECT a.serverId, a.is_actived FROM server_monitor_func_relation a, monitor_function b WHERE a.funcId = b.id AND b.module = "%s"' % inspect.stack()[0][3]
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in fows:
                serverId = row[0]
                is_actived = row[1]
                if is_actived == 1:
                    query = 'SELECT a.global_ip, b.username, b.password, c.port, c.is_actived FROM server_detail a, monitor_mysql_user b, server_service c WHERE a.serverId = b.serverId = c.serverId = "%s" AND c.name = "Mysql"' % serverId
                    cursor.execute(query)
                    row = cursor.fetchone()
                    global_ip = row[0]
                    username = row[1]
                    password = row[2]
                    ports = str(row[3]).replace('"', '').replace('[', '').replace(']', '').split(', ')
                    service_actived = row[4]
                    if service_actived == 1:
                        for port in ports:
                            remote_cursor = mysql_connector(global_ip, port, username, password)
                            datas = remote_cursor.select_all(sql)
                            record = repl_update_or_create(datas, serverId, port)
                    else:
                        msg = 'this Server have not acvtied Mysql monitor'
                        logger.info(msg)
                else:
                    msg = 'this Server have not acvtied this monitor function'
                    logger.info(msg)
    except Exception as e:
        logger.error(e)


@app.task(name='monitor.task.get_global_status')
def get_global_status():
    from monitor.mysql_library import status_create, status_querySet
    from monitor.connector import mysql_connector

    sql = "show global status"
    try:
        with connection.cursor() as cursor:
            query = 'SELECT a.serverId, a.is_actived FROM server_monitor_func_relation a, monitor_function b WHERE a.funcId = b.id AND b.module = "%s"' % inspect.stack()[0][3]
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in fows:
                serverId = row[0]
                is_actived = row[1]
                if is_actived == 1:
                    query = 'SELECT a.global_ip, b.username, b.password, c.port, c.is_actived FROM server_detail a, monitor_mysql_user b, server_service c WHERE a.serverId = b.serverId = c.serverId = "%s" AND c.name = "Mysql"' % serverId
                    cursor.execute(query)
                    row = cursor.fetchone()
                    global_ip = row[0]
                    username = row[1]
                    password = row[2]
                    ports = str(row[3]).replace('"', '').replace('[', '').replace(']', '').split(', ')
                    service_actived = row[4]
                    if service_actived == 1:
                        for port in ports:
                            remote_cursor = mysql_connector(global_ip, port, username, password)
                            datas = remote_cursor.select_all(sql)
                            status_dataset = status_querySet(datas)
                            record = status_create(status_dataset, serverId, port)
                    else:
                        msg = 'this Server have not acvtied Mysql monitor'
                        logger.info(msg)
                else:
                    msg = 'this Server have not acvtied this monitor function'
                    logger.info(msg)
    except Exception as e:
        logger.error(e)


@app.task(name='monitor.task.get_connections')
def get_connections():
    from monitor.mysql_library import connection_querySet, connection_update_or_create, connection_create
    from monitor.connector import mysql_connector

    sql = "show status like '%connect%'"
    try:
        with connection.cursor() as cursor:
            query = 'SELECT a.serverId, a.is_actived FROM server_monitor_func_relation a, monitor_function b WHERE a.funcId = b.id AND b.module = "%s"' % inspect.stack()[0][3]
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in fows:
                serverId = row[0]
                is_actived = row[1]
                if is_actived == 1:
                    query = 'SELECT a.global_ip, b.username, b.password, c.port, c.is_actived FROM server_detail a, monitor_mysql_user b, server_service c WHERE a.serverId = b.serverId = c.serverId = "%s" AND c.name = "Mysql"' % serverId
                    cursor.execute(query)
                    row = cursor.fetchone()
                    global_ip = row[0]
                    username = row[1]
                    password = row[2]
                    ports = str(row[3]).replace('"', '').replace('[', '').replace(']', '').split(', ')
                    service_actived = row[4]
                    if service_actived == 1:
                        for port in ports:
                            remote_cursor = mysql_connector(global_ip, port, username, password)
                            datas = remote_cursor.select_all(sql)
                            dataset = connection_querySet(datas)
                            record = connection_create(dataset, serverId, port)
                    else:
                        msg = 'this Server have not acvtied Mysql monitor'
                        logger.info(msg)
                else:
                    msg = 'this Server have not acvtied this monitor function'
                    logger.info(msg)
    except Exception as e:
        logger.error(e)
