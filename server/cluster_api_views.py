#!/usr/bin/python
# coding: utf-8
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .models import Cluster, ServerClusterRelate
from .serializers import ClusterSerializers, ServerClusterRelateSerializers

import json
import logging
# Create your views here.

logger = logging.getLogger('sourceDns.webdns.views')


class CreateCluster(APIView):

    def post(self, request, format=None):
        serializer = ClusterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCluster(APIView):

    def get_object_all(self):
        try:
            return Cluster.objects.all()
        except Exception as e:
            logger.error(e)

    def get_object_id(self, id):
        try:
            return Cluster.objects.get(id=id)
        except Exception as e:
            logger.error(e)

    def get_server(self, id):
        try:
            server = []
            with connection.cursor() as cursor:
                query = 'SELECT a.name FROM server a, server_cluster_relate b WHERE b.clusterId={clusterid} and a.id=b.serverId'.format(clusterid=id)
                cursor.execute(query)
                data = cursor.fetchall()
                if len(data) >=1:
                    for d in data:
                        server.append(d[0])
                return server
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        clusterid = json.loads(request.body).get('clusterid', None)

        if clusterid:
            cluster = self.get_object_id(clusterid)
            serializer = ClusterSerializers(cluster)
            if serializer.data:
                server = self.get_server(clusterid)
                data = {
                    'id': serializer.data.get('id'),
                    'name': serializer.data.get('name'),
                    'type': serializer.data.get('type'),
                    'region': serializer.data.get('region'),
                    'server': server
                }
                return Response(data)
            else:
                data = {
                    'retcode': -1,
                    'retmsg': 'fail to load data'
                }
                return Response(data)
        else:
            cluster = self.get_object_all()
            serializer = ClusterSerializers(cluster, many=True)
            datas = []
            if serializer.data:
                for data in serializer.data:
                    server = self.get_server(data.get('id'))
                    cluster = {
                        'id': data.get('id'),
                        'name': data.get('name'),
                        'type': data.get('type'),
                        'region': data.get('region'),
                        'server': server
                    }
                    datas.append(cluster)
                msg = {
                    'retcode': 0,
                    'retdata': datas
                    }
                return Response(msg)
            else:
                data = {
                    'retcode': -4,
                    'retmsg': 'fail to load data'
                }
                return Response(data)


class SetCluster(APIView):

    def get_object_id(self, id):
        try:
            return Cluster.objects.get(id=id)
        except Exception as e:
            logger.error(e)

    def update_object(self, object, name, type, region):
        try:
            object.update(name=name, type=type, region=region)
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        clusterid = json.loads(request.body).get('clusterid', None)
        if clusterid is None:
            raise ParamException('clusterid')

        name = json.loads(request.body).get('name', None)
        if name is None:
            raise ParamException('name')
        type = json.loads(request.body).get('type', None)
        if type is None:
            raise ParamException('type')
        region = json.loads(request.body).get('region', None)
        if region is None:
            raise ParamException('region')

        cluster = self.get_object_id(clusterid)
        if cluster:
            update = self.update_object(cluster, name, type, region)
            msg = {
                'retcode': 0,
                'retmsg': 'success'
            }
            return Response(msg)
        else:
            msg = {
                'retcode': -4,
                'retmsg': 'this record is not exist'
            }
            return Response(msg)


class DelCluster(APIView):

    def get_object_id(self, id):
        try:
            return Cluster.objects.get(id=id)
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        clusterid = json.loads(request.body).get('clusterid', None)
        if clusterid is None:
            raise ParamException('clusterid')

        cluster = self.get_object_id(clusterid)
        if cluster:
            delete = cluster.delete()
            msg = {
                'retcode': 0,
                'retmsg': 'success'
            }
            return Response(msg)
        else:
            msg = {
                'retcode': -4,
                'retmsg': 'this record is not exist'
            }
            return Response(msg)


class BindClusterServer(APIView):

    def post(self, request, format=None):
        clusterid = json.loads(request.body).get('clusterid', None)
        serverids = json.loads(request.body).get('serverids', None)

        datas = []

        if isinstance(serverids, list):
            for data in serverids:
                serverid = data
                data = {
                    'serverid': serverid,
                    'clusterid': clusterid
                }
                serializer = ServerClusterRelateSerializers(data=data)
                if serializer.is_valid():
                    serializer.save()
                    datas.append(serializer.data)
            if len(datas) >= 1:
                msg = {
                    'retcode': 0,
                    'retdata': datas,
                    'retmsg': 'success'
                }
                return Response(msg)
            else:
                msg = {
                    'retcode': -4,
                    'retmsg': 'this record is not exist'
                    }
                return Response(msg)
