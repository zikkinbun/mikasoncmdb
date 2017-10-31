# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .models import Mysql_Replication, Mysql_Status, Mysql_Connection, Mysql_Monitor
from .serializers import MysqlConnSerializers, MysqlMonitorSerializers, MysqlReplicationSerializers, MysqlStatusSerializers

import json
# Create your views here.

class MysqlStatus(APIView):

    def get_status(self):
        try:
            return Mysql_Status.objects.all()
        except Exception as e:
            print e

    def get_status_by_ip(self, ip):
        try:
            return Mysql_Status.objects.filter(db_ip=ip)
        except Exception as e:
            print e

    def post(self, request, format=None):
        ip = json.loads(request.body).get('ip', None)

        datas = self.get_status_by_ip(ip)
        serializer = MysqlStatusSerializers(datas, many=True)
        msg = {
            'retcode': 0,
            'retdata': serializer.data,
            'retmsg': 'success'
        }
        return Response(msg)

class MysqlConns(APIView):

    def get_conn_by_ip(self, ip):
        try:
            return Mysql_Connection.objects.filter(db_ip=ip).order_by('-create_time')
        except Exception as e:
            print e

    def serializer_data(self, object):
        return MysqlConnSerializers(master_datas, many=True)

    def post(self, request, format=None):
        ip = json.loads(request.body).get('ip', None)
        # print ip[0], ip[1]
        master_datas = self.get_conn_by_ip(ip[0])
        slave_datas = self.get_conn_by_ip(ip[1])

        master_serializer = MysqlConnSerializers(master_datas, many=True)
        slaves_serializer = MysqlConnSerializers(slave_datas, many=True)

        master_conns = []
        slave_conns = []
        # print master_serializer.data
        for conn in master_serializer.data:
            master_conns.append(int(conn['thead_connect']))
        master_conns.reverse()

        for conn in slaves_serializer.data:
            slave_conns.append(int(conn['thead_connect']))
        slave_conns.reverse()

        msg = {
            'retcode': 0,
            'retdata': {
                'master': master_conns,
                'slave': slave_conns
            },
            'retmsg': 'success'
        }
        return Response(msg)

class CreateMysqlMonitor(APIView):

    def create_mysql_monitor(self, ip, port, tag):
        try:
            return Mysql_Monitor.objects.create(db_ip=ip, db_port=port, tag=tag)
        except Exception as e:
            print e

    def post(self, request, format=None):
        db_ip = json.loads(request.body).get('ip', None)
        if db_ip is None:
            raise ParamException('ip')
        db_port = json.loads(request.body).get('port', None)
        if db_port is None:
            raise ParamException('port')
        server_tag = json.loads(request.body).get('server_tag', None)
        if server_tag is None:
            raise ParamException('server_tag')

        record = self.create_mysql_monitor(db_ip, db_port, server_tag)
        # print record

        msg = {
            'retcode': 0,
            'retmsg': 'success'
        }
        return Response(msg)

class GetMysqlMonitor(APIView):

    def get_monitor_all(self):
        try:
            return Mysql_Monitor.objects.all()
        except Exception as e:
            print e

    def post(self, request, format=None):

        datas = self.get_monitor_all()
        serializer = MysqlMonitorSerializers(datas, many=True)
        if datas:
            msg = {
                'retcode': 0,
                'retdata': serializer.data,
                'retmsg': 'success'
            }
            return Response(msg)
        else:
            msg = {
                'retcode': -1,
                'retmsg': 'get no data'
            }
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateMysqlMonitor(APIView):

    def active_all(self, db_ip):
        try:
            server = Mysql_Monitor.objects.filter(db_ip=db_ip)
            if server['db_user'] and server['db_pass']:
                return server.update(check_longsql=1, check_active=1, check_connections=1, check_delay=1, check_slave=1)
            else:
                raise BaseException(BaseError.ERROR_PASSWORD_NOT_EXIST)
        except Exception as e:
            print e

    def update_user_pass(self, db_ip, user, passwd):
        try:
            server = Mysql_Monitor.objects.filter(db_ip=db_ip)
            return server.update(db_user=user, db_pass=passwd)
        except Exception as e:
            print e

    def post(self, request, format=None):
        db_ip = json.loads(request.body).get('ip', None)
        if db_ip is None:
            raise ParamException('ip')
        db_user = json.loads(request.body).get('db_user', None)
        db_pass = json.loads(request.body).get('db_pass', None)

        if db_user and db_pass:
            update = self.update_user_pass(db_ip, db_user, db_pass)
            if update:
                msg = {
                    'retcode': 0,
                    'retmsg': 'update db user success'
                }
                return Response(msg)

        active = self.active_all(db_ip)
        if active:
            msg = {
                'retcode': 0,
                'retmsg': 'success'
            }
            return Response(msg)

        else:
            msg = {
                'retcode': -2,
                'retmsg': 'active failed'
            }
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
