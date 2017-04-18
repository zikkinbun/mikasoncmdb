# _*_ coding:utf-8_*_
from django.shortcuts import render, HttpResponse
import json
import redis

# Create your views here.
from zabbixapi.api import *

def test(request):
    mem_item_id = '23711'
    mem_data = gethistory_data(mem_item_id)
    value = []
    for host in mem_data:
        value.append(host[u'value'])
        # return HttpResponse(json.dumps(value))
    js_data = json.dumps(value)
    return render(request, 'test.html', locals())

def test_list(request):
    mem_item_list = ['23711', '23833', '23899', '23940', '23981', '24022', '23316']
    mem_data = get_data_count(itemlist=mem_item_list)
    time_data = gethistory_clock(itemlist=mem_item_list)
    js_data = json.dumps(mem_data)
    t_data = json.dumps(time_data)
    return render(request, 'test.html', locals())
    # return HttpResponse('ok')
