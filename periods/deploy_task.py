# _*_ coding:utf-8_*_
import os
import json
import time
import requests
from datetime import datetime
# from deploySystem.celery import app
from celery import task

from deploy.models import PeriodTask
from deploy.serializers import PeriodTaskSerializers
from deploy.internal_deploy_api import PeriodDeploy

@task()
def deployTask():
    try:
        tasks = PeriodTask.objects.all()
        serializer = PeriodTaskSerializers(tasks, many=True)
        for task in serializer.data:
            if task['status'] == 0:
                print task['period']
                # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                # if task['period'] == current_time:
                #     periodtask = PeriodDeploy(task['project'], task['branch'], task['tag'], task['env'], task['config'], task['type'])
                #     status = periodtask.run()
                #     if status['retcode'] == 0:
                #         PeriodTask.objects.filter(id=task['id']).update(status=1)
                #     else:
                #         PeriodTask.objects.filter(id=task['id']).update(status=2)
    except Exception as e:
        print e

# r = deployTask.delay()
