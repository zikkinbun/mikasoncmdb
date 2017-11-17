# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .models import MonitorMysqlConnection, MonitorMysqlProcesslist, MonitorMysqlReplication, MonitorMysqlStatus, MonitorMysqlSlowQueryHis
from .serializers import MysqlConnSerializers, MysqlReplicationSerializers, MysqlStatusSerializers

import json
import logging
# Create your views here.

logger = logging.getLogger('sourceDns.webdns.views')

class MysqlStatus(APIView):

    def get_status(self):
        try:
            return MonitorMysqlStatus.objects.all()
        except Exception as e:
            logger.error(e)

    def get_status_by_ip(self, ip):
        try:
            return MonitorMysqlStatus.objects.filter(db_ip=ip)
        except Exception as e:
            logger.error(e)

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

class MysqlCom(APIView):

    def get_com_data(self, ip):
        try:
            com_object = MonitorMysqlStatus.objects.filter(db_ip=ip).order_by('-create_time')[:100]
            serializer = MysqlStatusSerializers(com_object, many=True)
            Com_select = []
            Com_insert = []
            Com_update = []
            Com_commit = []
            Com_rollback = []
            Com_delete = []
            query = []
            for data in serializer.data:
                Com_select.append(int(data['com_select']))
                Com_insert.append(int(data['com_insert']))
                Com_update.append(int(data['com_update']))
                Com_commit.append(int(data['com_commit']))
                Com_rollback.append(int(data['com_rollback']))
                Com_delete.append(int(data['com_delete']))
                query.append(int(data['queries']))
            response = {
                'com_select': Com_select,
                'com_insert': Com_insert,
                'com_update': Com_update,
                'com_commit': Com_commit,
                'com_rollback': Com_rollback,
                'com_delete': Com_delete,
                'queries': query
            }
            return response
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        ip = json.loads(request.body).get('ip', None)
        if ip is None:
            raise ParamException('ip')

        data = self.get_com_data(ip)
        if data:
            msg = {
                'retcode': 0,
                'retdata': data,
                'retmsg': 'success'
            }
            return Response(msg)

class MysqlConns(APIView):

    def get_conn_by_ip(self, ip):
        try:
            return MonitorMysqlConnection.objects.filter(db_ip=ip).order_by('-create_time')[:10]
        except Exception as e:
            logger.error(e)

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
