# _*_ coding:utf-8_*_
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

import time
import json
import urllib2

from .serializers import CpuLoadSerializers, MemStatSerializers, HddStatSerializers
from .models import MonitorCpuLoad, MonitorHddStat, MonitorMemStat
# Create your views here.

def processData(method, params):
    url = 'http://120.77.46.79:8001/api_jsonrpc.php'
    header = {"Content-Type":"application/json"}
    data = {
        "jsonrpc": "2.0",
        "method": "",
        "params": {},
        "auth": "5e7f7d055a05f3bfb9abecd77f9f0381",
        "id": 1
    }
    data['method'] = method
    data['params'] = params
    post_data = json.dumps(data)
    request_data = urllib2.Request(url, post_data)
    for key in header:
        request_data.add_header(key, header[key])
    try:
        result = urllib2.urlopen(request_data)
    except Exception as e:
        print (e)
    else:
        response = json.loads(result.read())
        return response['result']

class CpuLoadListAll(APIView):
    """
        list all data
    """

    def post(self, request, format=None):
        datas = MonitorCpuLoad.objects.all()[:10]
        serializer = CpuLoadSerializers(datas, many=True)
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
        datas = MonitorCpuLoad.objects.filter(hostip=hostip).order_by('-created')[:10]
        serializer = CpuLoadSerializers(datas, many=True)
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
        datas = MonitorMemStat.objects.all()[:10]
        serializer = MemStatSerializers(datas, many=True)
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
        datas = MonitorMemStat.objects.filter(hostip=hostip).order_by('-created')[:10]
        serializer = MemStatSerializers(datas, many=True)
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)

class GetBootTime(APIView):

    def post(self, request, format=None):
        itemlist = ['23688', '23810', '23876', '23917', '23958', '23999', '23293']
        namelist = ['get_dev', 'gdr_test', 'gdr_rd_prod', 'gdr_sql_mt', 'gdr_sql_sl', 'gdr_web_prod', 'zabbix_server']
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
            # print origin
            for host in origin:
                # print host
                day = int(host[u'value'])
                data[namelist[i]] = day
        series_data = []
        for name in namelist:
            series_data.append(data[name])
        r = {
            'retcode': 0,
            'retdata': series_data
        }
        return Response(r)

class GetUptime(APIView):

    def post(self, request, format=None):
        itemlist = ['23708', '23830', '23896', '23937', '23978', '24019', '23313']
        namelist = ['get_dev', 'gdr_test', 'gdr_rd_prod', 'gdr_sql_mt', 'gdr_sql_sl', 'gdr_web_prod', 'zabbix_server']
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
            # print origin
            for host in origin:
                # print type(host)
                day = int(host[u'value'])/(60*60*24) + 1
                data[namelist[i]] = day
        series_data = []
        for name in namelist:
            series_data.append(data[name])
        r = {
            'retcode': 0,
            'retdata': series_data
        }
        return Response(r)

class GetRunProcess(APIView):

    def post(self, request, format=None):
        itemlist = ['23687', '23809', '23875', '23916', '23957', '23998', '23292']
        namelist = ['get_dev', 'gdr_test', 'gdr_rd_prod', 'gdr_sql_mt', 'gdr_sql_sl', 'gdr_web_prod', 'zabbix_server']
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
            # print origin
            for host in origin:
                # print host
                proc = int(host[u'value'])
                data[namelist[i]] = proc
        series_data = []
        for name in namelist:
            series_data.append(data[name])
        r = {
            'retcode': 0,
            'retdata': series_data
        }
        return Response(r)
