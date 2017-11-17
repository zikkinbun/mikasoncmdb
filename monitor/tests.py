# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from connector import mysql_connector
# Create your tests here.

def thread_conn():

    sql = "show status like '%connect%'"
    master = {
        'host': '39.108.131.173',
        'port': 3306
    }
    cursor = mysql_connector(master['host'], master['port'], 'db_writer', '8^>ozBE?A.Zw')
    datas = cursor.select_all(sql)
    print datas

def checksum():
    master = {
        'host': '39.108.131.173',
        'port': 3306,
        'user': 'repl_user',
        'passwd': 'TSY8TjexUT7z'
    }
    slave = {
        'host': '39.108.177.246',
        'port': 3306,
        'user': 'repl_user',
        'passwd': 'TSY8TjexUT7z'
    }

    checksums = 'pt-table-checksum --user=slave --password=i9+ztAb:nW*K \
--host=192.168.1.214 --port=3306 \
--databases=gdrPlatform --tables=gdr_user --recursion-method=processlist \
--no-check-binlog-format --nocheck-replication-filters \
--replicate=percona.checksums'

    sync = ' pt-table-sync --replicate=yayun.checksums h=127.0.0.1,u=root,p=123456 h=192.168.0.20,u=root,p=123456 --execute'

    sql = 'select * from percona.checksums'

def slowlog():
    cmd = 'pt-query-digest --user=repl_user --password=TSY8TjexUT7z --review  h=192.168.1.214,D=percona_schema,t=query_review iZ94c5ah3t7Z-slow.log'

def deadlock():
    cmd = 'pt-deadlock-logger  --user=repl_user --password=TSY8TjexUT7z h=192.168.1.214,D=percona_schema,t=deadlocks'

if __name__ == '__main__':
    thread_conn()
