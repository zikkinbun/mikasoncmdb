# _*_ coding:utf-8_*_
import os
import json
import requests
from datetime import datetime
from celery import task

# from asset.models import Server, Server_Service, Server_NetWorkStatus
import config


@task
def check_tcp_status():
    Hosts = config.SERVERS.get('HOST')
    module = config.MODULES.get('TCPSTATUS')
    for host in Hosts:
        url = config.INTERFACE.replace('HOST:PORT', host) + module
        r = requests.post(url)
        data = r.json()
        print data

if __name__ == '__main__':
    check_tcp_status()
