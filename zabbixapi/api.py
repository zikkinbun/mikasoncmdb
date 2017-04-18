# _*_ coding:utf-8_*_
# The Auth ID Is: 5e7f7d055a05f3bfb9abecd77f9f0381
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from asset.models import Server

import json
import urllib2
import pymysql
import redis
import time

def processData(method, params):
    url = 'http://112.74.164.242:8001/api_jsonrpc.php'
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

@csrf_exempt
def get_uptime(request):
    if request.method == 'GET':
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
        r = json.dumps(series_data, encoding='utf-8')
        return HttpResponse(r)

@csrf_exempt
def get_boottime(request):
    if request.method == 'GET':
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
        r = json.dumps(series_data, encoding='utf-8')
        return HttpResponse(r)

@csrf_exempt
def agent_ping(request):
    if request.method == 'GET':
        itemlist = ['23682', '23804', '23870', '23911', '23952', '23993', '23287']
        namelist = ['gdr_dev', 'gdr_test', 'gdr_rd_prod', 'gdr_sql_mt', 'gdr_sql_sl', 'gdr_web_prod', 'zabbix_server']
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
            ping = data[server.Name]
            # print type(ping)
            if ping == int(1):
                Server.objects.filter(Name=server.Name).update(Status='在线')
            else:
                Server.objects.filter(Name=server.Name).update(Status='不在线')

        return HttpResponse("{'data': '请求成功'}")

@csrf_exempt
def get_runprocess(request):
    if request.method == 'GET':
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
        r = json.dumps(series_data, encoding='utf-8')
        return HttpResponse(r)
