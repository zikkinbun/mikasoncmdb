#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from server.models import Server
from server.serializers import ServerSerializers
from .models import Module, ModuleDetail, ModuleServerRelate
from .serializers import ModuleSerializers, ModuleDetailSerializers, ModuleServerRelateSerializers

import json
import logging
# Create your views here.

logger = logging.getLogger('sourceDns.webdns.views')

class CreateModule(APIView):

    def post(self, request, format=None):
        serializer = ModuleSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetModule(APIView):

    def get_object_id(self, id):
        try:
            return Module.objects.get(id=id)
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        moduleid = json.loads(request.body).get('moduleid', None)
        if moduleid is None:
            raise ParamException('moduleid')
        name = json.loads(request.body).get('name', None)
        if name is None:
            raise ParamException('name')
        type = json.loads(request.body).get('type', None)
        if type is None:
            raise ParamException('type')
        version = json.loads(request.body).get('version', None)
        if version is None:
            raise ParamException('version')

        module = self.get_object_id(moduleid)

        module_dict = {
            'id': moduleid,
            'name': name,
            'type': type,
            'version': version
        }

        serializer = ModuleSerializers(module, data=module_dict)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetModule(APIView):

    def get_object_all(self):
        try:
            return Module.objects.all()
        except Exception as e:
            logger.error(e)

    def get_object_id(self, id):
        try:
            return Module.objects.get(id=id)
        except Exception as e:
            logger.error(e)

    def get_module_relate_server(self, id):
        try:
            server_relat_object = ModuleServerRelate.objects.filter(moduleid=id)
            serializer = ModuleServerRelateSerializers(server_relat_object, many=True)
            servers = []
            for data in serializer.data:
                server_id = data.get('serverid')
                server = Server.objects.get(id=server_id)
                serializer = ServerSerializers(server)
                server = {
                    'id': serializer.data.get('id'),
                    'name': serializer.data.get('name')
                }
                servers.append(server)
            return servers
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        id = json.loads(request.body).get('id', None)

        if id:
            module = self.get_object_id(id)
            moduleserializer = ModuleSerializers(module)
            servers = self.get_module_relate_server(id)
            module = moduleserializer.data
            module['servers'] = servers
            msg = {
                'retcode': 0,
                'retdata': module
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            module = self.get_object_all()
            moduleserializer = ModuleSerializers(module, many=True)
            moduleList = []
            for data in moduleserializer.data:
                servers = self.get_module_relate_server(data.get('id'))
                module = {
                    'id': data.get('id'),
                    'name': data.get('name'),
                    'type': data.get('type'),
                    'version': data.get('version'),
                    'servers': servers
                }
                moduleList.append(module)
            msg = {
                'retcode': 0,
                'retdata': moduleList
            }
            return Response(msg, status=status.HTTP_201_CREATED)


class CreateModuleDetail(APIView):

    def post(self, request, format=None):
        serializer = ModuleDetailSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetModuleDetail(APIView):

    def get_detail(self, serverid, moduleid):
        try:
            with connection.cursor() as cursor:
                query = 'SELECT moduleId,serverId FROM module_detail WHERE moduleId={moduleid} AND serverId={serverid}'.format(moduleid=moduleid, serverid=serverid)
                cursor.execute(query)
                data = cursor.fetchone()
                return data
        except Exception as e:
            logger.error(e)

    def create_detail(self, port, configfile, serverid, moduleid):
        module_dict = {
            'moduleid': moduleid,
            'serverid': serverid,
            'port': port,
            'configfile': configfile
        }
        serializer = ModuleDetailSerializers(data=module_dict)
        if serializer.is_valid():
            serializer.save()
            return 1
        else:
            return 0

    def update_detail(self, port, configfile, serverid, moduleid):
        try:
            with connection.cursor() as cursor:
                query = "UPDATE module_detail SET port='{port}',configfile='{configfile}'  WHERE moduleId={moduleid} AND serverId={serverid}".format(port=port, configfile=configfile, moduleid=moduleid, serverid=serverid)
                cursor.execute(query)
            connection.commit()
            connection.close()
        except Exception as e:
            connection.rollback()
            logger.error(e)

    def post(self, request, format=None):
        moduleid = json.loads(request.body).get('moduleid', None)
        if moduleid is None:
            raise ParamException('moduleid')
        serverid = json.loads(request.body).get('serverid', None)
        if serverid is None:
            raise ParamException('serverid')
        port = json.loads(request.body).get('port', None)
        if port is None:
            raise ParamException('port')
        configfile = json.loads(request.body).get('configfile', None)
        if configfile is None:
            raise ParamException('configfile')

        detail = self.get_detail(serverid, moduleid)
        if detail:
            self.update_detail(port, configfile, serverid, moduleid)
            msg = {
                'retcode': 0,
                'retmsg': 'success'
                }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            row = self.create_detail(port, configfile, serverid, moduleid)
            if row:
                msg = {
                    'retcode': 0,
                    'retmsg': 'success'
                    }
                return Response(msg, status=status.HTTP_201_CREATED)
            else:
                msg = {
                        'retcode': -2,
                        'retmsg': 'update fail'
                        }
                return Response(msg)


class GetModuleDetail(APIView):

    def get_object_id(self, id):
        try:
            return ModuleDetail.objects.get(moduleid=id)
        except Exception as e:
            logger.error(e)

    def get_module_server(self, server_id, module_id):
        try:
            with connection.cursor() as cursor:
                query = 'SELECT port, is_actived, configfile FROM module_detail WHERE moduleid={module} AND serverid={server}'.format(module=module_id, server=server_id)
                cursor.execute(query)
                row = cursor.fetchone()
                data = {
                    'id': module_id,
                    'serverid': server_id,
                    'port': str(row[0]).replace('"', '').replace('[', '').replace(']', '').split(', '),
                    'is_actived': row[1],
                    'configfile': row[2]
                }
                return data
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):

        moduleId = json.loads(request.body).get('moduleid', None)
        if moduleId is None:
            raise ParamException('moduleid')

        serverId = json.loads(request.body).get('serverid', None)
        if moduleId is None:
            raise ParamException('serverid')

        data = self.get_module_server(moduleId, serverId)
        if data:
            datas = []
            datas.append(data)
            msg = {
                'retcode': 0,
                'retdata': datas
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            msg = {
                'retcode': -1,
                'retmsg': 'this record is not exist'
            }
            return Response(msg, status=status.HTTP_201_CREATED)


class ActiveDetail(APIView):

    def active_detail(self, moduleid, serverid, is_actived):
        try:
            with connection.cursor() as cursor:
                query = 'UPDATE module_detail SET is_actived={is_actived} WHERE moduleId={moduleid} AND serverId={serverid}'.format(is_actived=is_actived, moduleid=moduleid, serverid=serverid)
                row = cursor.execute(query)
            return row
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        moduleid = json.loads(request.body).get('moduleid', None)
        if moduleid is None:
            raise ParamException('moduleid')
        serverid = json.loads(request.body).get('serverid', None)
        if serverid is None:
            raise ParamException('serverid')
        is_actived = json.loads(request.body).get('is_actived', None)
        if is_actived is None:
            raise ParamException('is_actived')

        active = self.active_detail(moduleid, serverid, is_actived)
        if active:
            msg = {
                'retcode': 0,
                'retmsg': 'success'
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            msg = {
                'retcode': -1,
                'retmsg': 'this record is not exist'
            }
            return Response(msg, status=status.HTTP_201_CREATED)


class SetModuleServer(APIView):

    def post(self, request, format=None):
        serializer = ModuleServerRelateSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteModule(APIView):

    def get_module_object(self, module_id):
        try:
            return Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            raise Http404

    def get_detail_object(self, module_id):
        try:
            return ModuleDetail.objects.get(moduleid=module_id)
        except ModuleDetail.DoesNotExist:
            raise Http404

    def get_module_server_object(self, module_id):
        try:
            return ModuleServerRelate.objects.get(moduleid=module_id)
        except ModuleServerRelate.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        moduleid = json.loads(request.body).get('moduleid', None)
        if moduleid is None:
            raise ParamException('moduleid')

        module = self.get_module_object(moduleid)
        detail = self.get_detail_object(moduleid)
        relate = self.get_module_server_object(moduleid)
        module.delete()
        detail.delete()
        relate.delete()
        if self.get_module_object(moduleid):
            msg = {
                'retcode': -1,
                'retmsg': 'fail to delete'
            }
            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        else:
            msg = {
                'retcode': 0,
                'retmsg': 'success'
            }
            return Response(msg)
