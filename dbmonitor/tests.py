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

if __name__ == '__main__':
    thread_conn()
