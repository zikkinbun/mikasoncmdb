#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Records, PeriodTask
from .serializers import PeriodTaskSerializers, RecordsSerializers
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .gitlab_api import *
from .salt_api import *

import time
import subprocess
import shutil
import json
import os

class PeriodDeploy(APIView):

    def create_period(self, task):
        try:
            return PeriodTask.objects.create(name=task['name'], project=task['project'], branch=task['branch'], \
                tag=task['tag'], env=task['env'], config=task['config'], type=task['type'], period=task['crontab'], status=task['status'])
        except Exception as e:
            print e

    def post(self, request, format=None):
        # print request.body

        name = json.loads(request.body).get('name', None)
        if name is None:
            raise ParamException('name')
        project = json.loads(request.body).get('project', None)
        if project is None:
            raise ParamException('project')
        branch = json.loads(request.body).get('branch', None)
        if branch is None:
            raise ParamException('branch')
        tag = json.loads(request.body).get('tag', None)
        if tag is None:
            raise ParamException('tag')
        env = json.loads(request.body).get('env', None)
        if env is None:
            raise ParamException('env')
        if env == u'生产环境':
            env = 'prod'
        else:
            env = 'test'
        config = json.loads(request.body).get('config', None)
        if config is None:
            raise ParamException('config')
        type = json.loads(request.body).get('type', None)
        if type is None:
            raise ParamException('type')
        crontab_date = json.loads(request.body).get('date', None)
        if crontab_date is None:
            raise ParamException('date')
        crontab_time = json.loads(request.body).get('time', None)
        if crontab_time is None:
            raise ParamException('time')

        date = time.strftime("%Y-%m-%d", time.localtime(float(str(crontab_date)[:10])))
        current = time.strftime("%H:%M", time.localtime(float(str(crontab_time)[:10])))

        task = {
            'name': name,
            'project': project,
            'branch': branch,
            'tag': tag,
            'env': env,
            'config': config,
            'type': type,
            'crontab': date + ' ' + current,
            'status': 0
        }
        # status状态码：0 = 未执行 1 = 执行成功 2 = 执行失败
        print task

        new_task = self.create_period(task)

        msg = {
            'retcode': 0,
            'retmsg': 'success'
        }
        return Response(msg)
