# _*_ coding:utf-8_*_
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError
import json

from .serializers import cpuloadSerializers, cpustatSerializers, memstatSerializers
from .models import cpuload, cpustat, memstat
# Create your views here.

class CpuStatList(APIView):
    """
        list all data
    """

    def post(self, request, format=None):
        datas = cpustat.objects.all()[:10]
        serializer = cpustatSerializers(datas, many=True)
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)

class CpuLoadListAll(APIView):
    """
        list all data
    """

    def post(self, request, format=None):
        datas = cpuload.objects.all()[:10]
        serializer = cpuloadSerializers(datas, many=True)
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)

class CpuLoadListByIP(APIView):

    def post(self, request, format=None):
        hostip = json.loads(request.body).get('hostip', None)
        if hostip is None:
            raise ParamException('hostip')
        # print hostip
        datas = cpuload.objects.filter(hostip=hostip).order_by('-created')[:10]
        serializer = cpuloadSerializers(datas, many=True)
        # print serializer.data
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)

class MemStatListAll(APIView):
    """
        list all data
    """

    def post(self, request, format=None):
        datas = memstat.objects.all()[:10]
        serializer = memstatSerializers(datas, many=True)
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)

class MemStatListByIP(APIView):

    def post(self, request, format=None):
        hostip = json.loads(request.body).get('hostip', None)
        if hostip is None:
            raise ParamException('hostip')
        # print hostip
        datas = memstat.objects.filter(hostip=hostip).order_by('-created')[:10]
        serializer = memstatSerializers(datas, many=True)
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)
