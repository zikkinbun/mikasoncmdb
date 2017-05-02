# _*_ coding:utf-8_*_
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

import json

from .serializers import cpuloadSerializers, cpustatSerializers, memstatSerializers
from .models import cpuload, cpustat, memstat
# Create your views here.

class CpuStatList(APIView):
    """
        list all data
    """

    def get(self, request, format=None):
        datas = cpustat.objects.all()[:10]
        serializer = cpustatSerializers(datas, many=True)
        return Response(serializer.data)

class CpuLoadList(APIView):
    """
        list all data
    """

    def get(self, request, format=None):
        datas = cpuload.objects.all()[:10]
        serializer = cpuloadSerializers(datas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        hostip = request.data.get('hostip')
        # print hostip
        datas = cpuload.objects.filter(hostip=hostip)[:10]
        serializer = cpuloadSerializers(datas, many=True)
        return Response(serializer.data)

class MemStatList(APIView):
    """
        list all data
    """

    def get(self, request, format=None):
        datas = memstat.objects.all()[:10]
        serializer = memstatSerializers(datas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        hostip = request.data.get('hostip')
        # print hostip
        datas = memstat.objects.filter(hostip=hostip)[:10]
        serializer = memstatSerializers(datas, many=True)
        return Response(serializer.data)
