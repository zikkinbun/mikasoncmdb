# _*_ coding:utf-8_*_
# The Auth ID Is: 5e7f7d055a05f3bfb9abecd77f9f0381
import json
import urllib2
import pymysql
import redis
import time

def conndb():
    conn = pymysql.connect(host='112.74.182.80', port='3306', user='gdrAdmin', password='gdr2016', db='', charset='utf8')
    cur = conn.cursor()
    return cur

def connrd(db=None):
    conn = redis.Redis(host='112.74.182.80', port=6379, password='gdrdev2016', db=db)
    return conn

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

def get_data_count(itemlist=None):
    """
        先将数据进行计算再存进redis db1
    """
    method = "history.get"
    redis = connrd(db=1)
    if itemlist:
        for item in itemlist:
            params = {
                "output": "extend",
                "history": 3,
                "itemids": item,
                "limit": 10
            }
            data = processData(method, params)
            k = 1024
            m = 1024*k
            redis.set(item, json.dumps([int(host[u'value'])/m for host in data]))
    else:
        msg = 'empty list'
        return msg
    data = {item: redis.get(item) for item in itemlist}
    # print data
    return data

def get_data(itemlist=None):
    """
        直接将数据存进redis db1
    """
    method = "history.get"
    redis = connrd(db=1)
    if itemlist:
        for item in itemlist:
            params = {
                "output": "extend",
                "history": 3,
                "itemids": item,
                "limit": 10
            }
            data = processData(method, params)
            redis.set(item, json.dumps([(host[u'value']) for host in data]))
    else:
        msg = 'empty list'
        return msg
    data = {item: redis.get(item) for item in itemlist}
    # print data
    return data

def gethistory_clock(itemlist=None):
        """
            先将数据存进redis db1
        """
        method = "history.get"
        redis = connrd(db=2)
        if itemlist:
            for item in itemlist:
                params = {
                    "output": "extend",
                    "history": 3,
                    "itemids": item,
                    "limit": 10
                }
                data = processData(method, params)
                clocks = []
                for host in data:
                    clocks.append(host[u'clock'])
                new_clocks = []
                for clock in clocks:
                    strtime = time.strftime("%Y%m%d%H%M", time.gmtime(float(clock)))
                    new_clocks.append(strtime)
                redis.set(item, json.dumps(new_clocks))
        else:
            msg = 'empty list'
            return msg
        data = {item: redis.get(item) for item in itemlist}
        # print data
        return data


def get_uptime(itemlist=None):
    method = "history.get"
    redis = connrd(db=3)
    if itemlist:
        for item in itemlist:
            value = []
            params = {
                    "output": "extend",
                    "history": 3,
                    "itemids": item,
                    "limit": 10
            }
            origin = processData(method, params)
            for host in origin:
                value.append(host[u'value'])
                redis.set(item, json.dumps(value))
    else:
        msg = 'empty list'
        return msg
    data = {item: redis.get(item) for item in itemlist}
    return data
