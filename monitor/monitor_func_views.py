# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .models import MonitorFunction
from .serializers import MonitorFunctionSerializers

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
