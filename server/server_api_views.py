# coding: utf-8
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .models import Server, ServerDetail, ServerSevice, ServerMonitorFuncRelation
from .serializers import ServerSerializers, ServerDetailSerializers, ServerSeviceSerializers, ServerMonitorFuncRelationSerializers
import json
import logging
# Create your views here.

logger = logging.getLogger('sourceDns.webdns.views')

class ListServer(APIView):
    """
        list all servers or create a server
    """

    def post(self, request, format=None):
        servers = Server.objects.all()
        serializer = ServerSerializers(servers, many=True)
        # print serializer.data
        data = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(data)


class CreateServer(APIView):

    def post(self, request, format=None):
        data = {
            'name': json.loads(request.body).get('name', None),
            'alias': json.loads(request.body).get('alias', None),
            'tag': json.loads(request.body).get('tag', None),
            'status': json.loads(request.body).get('status', None),
            'is_monitor': json.loads(request.body).get('is_monitor', None)
        }
        # print data
        serializer = ServerSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditServer(APIView):
    """
        look up the detail server or update a sevser
    """

    def get_object(self, serverId):
        try:
            return Server.objects.get(id=serverId)
        except ServerDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')
        server = self.get_object(serverId)
        serializer = ServerSerializers(server, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteServer(APIView):

    def get_object(self, serverId):
        try:
            return Server.objects.get(id=serverId)
        except ServerDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')
        server = self.get_object(serverId)
        server.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateServerDetail(APIView):

    def post(self, request, format=None):

        data = {
            'serverId': json.loads(request.body).get('serverId', None),
            'cpu': json.loads(request.body).get('cpu', None),
            'mem': json.loads(request.body).get('mem', None),
            'netflow': json.loads(request.body).get('netflow', None),
            'hdd': json.loads(request.body).get('hdd', None),
            'system': json.loads(request.body).get('system', None),
            'core': json.loads(request.body).get('core', None),
        }
        serializer = ServerDetailSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetServerDetail(APIView):

    def get_object(self, serverId):
        try:
            query = 'SELECT a.id,a.name,a.alias,a.tag,b.cpu,b.mem,b.netflow,b.hdd,b.system,b.core FROM server a,server_detail b WHERE a.id=b.serverId and b.serverId=%s' % serverId
            return ServerDetail.objects.raw(query)
        except ServerDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')
        server = self.get_object(serverId)
        # print server
        serializer = ServerDetailSerializers(server, many=True)
        # print serializer.data
        data = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(data)


class EditServerDetail(APIView):
    """
        look up the detail server or update a sevser
    """

    def get_object(self, serverId):
        try:
            return ServerDetail.objects.get(serverId=serverId)
        except ServerDetail.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')
        server = self.get_object(serverId)
        serializer = ServerDetailSerializers(server, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateServerSevice(APIView):

    def post(self, request, format=None):
        """
            project_id: 0 为系统底层或第三方服务，其余为 gitlab 上的项目
        """
        data = {
            'serverId': json.loads(request.body).get('serverId', None),
            'projectId': json.loads(request.body).get('projectId', None),
            'name': json.loads(request.body).get('name', None),
            'port': json.loads(request.body).get('port', None),
            'version': json.loads(request.body).get('version', None),
            'is_actived': json.loads(request.body).get('is_actived', None)
        }
        serializer = ServerSeviceSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditServerSevice(APIView):
    """
        look up the detail server or update a sevser
    """

    def get_object(self, serverId):
        try:
            return ServerSevice.objects.get(serverId=serverId)
        except ServerSevice.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')
        sevice = self.get_object(serverId)
        serializer = ServerSeviceSerializers(sevice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetServerService(APIView):

    def get_object(self, serverId):
        try:
            return ServerSevice.objects.filter(serverId=serverId)
        except ServerSevice.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')
        service = self.get_object(serverId)
        # print server
        serializer = ServerSeviceSerializers(service, many=True)
        # print serializer.data
        datas = []
        for data in serializer.data:
            service = {
                'serverId': data.get('serverId', None),
                'name': data.get('name', None),
                'port': str(data.get('port', None)).replace('"', '').replace('[', '').replace(']', '').split(', '),
                'version': data.get('version', None),
                'is_actived': data.get('is_actived', None),
            }
            datas.append(service)
        services = {
            'retcode': 0,
            'retdata': datas
        }
        return Response(services)


class DeleteServerService(APIView):

    def get_object(self, serverId):
        try:
            return ServerSevice.objects.get(id=serverId)
        except ServerSevice.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')
        service = self.get_object(serverId)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServerFuncRelation(APIView):

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')

        funcId = json.loads(request.body).get('funcId', None)
        if funcId is None:
            raise ParamException('funcId')

        data = {
            'serverId': serverId,
            'funcId': funcId
        }

        serializer = ServerMonitorFuncRelationSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateActive(APIView):

    def update_active(self, serverId, funcId, active):
        try:
            func = ServerMonitorFuncRelation.objects.filter(serverId=serverId, funcId=funcId)
            if func:
                func.update(is_actived=active)
                return func
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')

        funcId = json.loads(request.body).get('funcId', None)
        if funcId is None:
            raise ParamException('funcId')

        is_actived = json.loads(request.body).get('is_actived', None)
        if is_actived is None:
            raise ParamException('is_actived')

        update = self.update_active(serverId, funcId, is_actived)
        if update:
            msg = {
                'retcode': 0,
                'retmsg': 'success'
            }
            return Response(msg)


class GetServerFunc(APIView):

    def get_server_func_by_id(self, serverId):
        try:
            datas = []
            with connection.cursor() as cursor:
                cursor.execute("SELECT b.name,b.module FROM server_monitor_func_relation a, monitor_function b WHERE a.serverId = %s AND a.funcId = b.id AND a.is_actived = 1", serverId)
                row = cursor.fetchall()
                for data in row:
                    func = {
                        'name': data[0],
                        'module': data[1]
                    }
                    datas.append(func)
                return datas
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        serverId = json.loads(request.body).get('serverId', None)
        if serverId is None:
            raise ParamException('serverId')

        func = self.get_server_func_by_id(serverId)
        # print func
        data = {
            'retcode': 0,
            'retdata': func
        }
        return Response(data)
