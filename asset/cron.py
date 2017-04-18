#!/usr/bin/python
# _*_ coding:utf-8_*_
from models import Server
from zabbixapi.api import processData

# Create your views here.

def agent_ping():
    itemlist = ['23682', '23804', '23870', '23911', '23952', '23993', '23287']
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
        for host in origin:
            ping = int(host[u'value'])
            data[namelist[i]] = ping
    servers = Server.objects.all()
    for server in servers:
        ping = data[server.Name]
        if ping == int(1):
            Server.objects.filter(Name=server.Name).update(Status='在线')
        else:
            Server.objects.filter(Name=server.Name).update(Status='不在线')

# if __name__ == '__main__':
#     agent_ping()
