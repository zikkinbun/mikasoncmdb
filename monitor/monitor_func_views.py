# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .models import MonitorFunction, MonitorMysqlUser
from .serializers import MonitorFunctionSerializers, MonitorMysqlUserSerializers

import json
import logging

logger = logging.getLogger('sourceDns.webdns.views')

class CreateMonitorFunction(APIView):

    def post(self, request, format=None):

        name = json.loads(request.body).get('name', None)
        if name is None:
            raise ParamException('name')
        comment = json.loads(request.body).get('comment', None)

        data = {
            'name': name,
            'comment': comment
        }
        serializer = MonitorFunctionSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMonitorFunction(APIView):

    def get_object(self):
        try:
            return MonitorFunction.objects.all()
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):

        func = self.get_object()
        serializer = MonitorFunctionSerializers(func, many=True)
        if func:
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMonitorMysqlUser(APIView):

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')
        username = json.loads(request.body).get('username', None)
        if username is None:
            raise ParamException('username')
        password = json.loads(request.body).get('password', None)
        if password is None:
            raise ParamException('password')
        tag = json.loads(request.body).get('tag', None)
        if tag is None:
            raise ParamException('tag')

        data = {
            'serverId': serverId,
            'username': username,
            'password': password,
            'tag': tag
        }
        serializer = MonitorMysqlUserSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMonitorMysqlUser(APIView):

    def get_object(self, serverId):
        try:
            return MonitorMysqlUser.objects.filter(serverId=serverId)
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')        
        user = self.get_object(serverId)
        serializer = MonitorMysqlUserSerializers(user, many=True)
        if user:
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
