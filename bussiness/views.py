#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals

from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .models import Bussiness, BussinessData, BussinessTopu
from deployuser.models import CustomUser
from .serializers import BussinessSerializers, BussinessDataSerializers, BussinessTopuSerializers

import json


class CreateBussiness(APIView):

    def post(self, request, format=None):
        serializer = BussinessSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBussiness(APIView):

    def get_object_all(self):
        try:
            return Bussiness.objects.all()
        except Exception as e:
            logger.error(e)

    def get_object_id(self, id):
        try:
            return Bussiness.objects.get(id=id)
        except Exception as e:
            logger.error(e)

    def get_user(self, id):
        try:
            user = CustomUser.objects.get(id=id)
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone
            }
            return data
        except Exception as e:
            print e

    def post(self, request, format=None):
        id = json.loads(request.body).get('id', None)

        if id:
            bussiness = self.get_object_id(id)
            operator = self.get_user(bussiness.operatorid)
            productor = self.get_user(bussiness.productorid)
            serializer = BussinessSerializers(bussiness)
            data = {
                'id': serializer.data.get('id'),
                'name': serializer.data.get('name'),
                'type': serializer.data.get('type'),
                'hostnum': serializer.data.get('hostnum'),
                'operator': operator.get('username'),
                'productor': productor.get('username'),
                'creator': serializer.data.get('creator')
            }
            msg = {
                'retcode': 0,
                'retdata': data
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            bussiness = self.get_object_all()
            serializer = BussinessSerializers(bussiness, many=True)
            datas = []
            for bus in serializer.data:
                operator = self.get_user(bus.get('operatorid'))
                productor = self.get_user(bus.get('productorid'))
                data = {
                    'id': bus.get('id'),
                    'name': bus.get('name'),
                    'type': bus.get('type'),
                    'hostnum': bus.get('hostnum'),
                    'operator': operator.get('username'),
                    'productor': productor.get('username'),
                    'creator': bus.get('creator')
                }
                datas.append(data)
            msg = {
                'retcode': 0,
                'retdata': datas
            }
            return Response(msg, status=status.HTTP_201_CREATED)


class DelBussiness(APIView):

    def get_object_id(self, id):
        try:
            return Bussiness.objects.get(id=id)
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):
        bussinessid = json.loads(request.body).get('bussinessid', None)
        if bussinessid is None:
            raise ParamException('bussinessid')

        bussiness = self.get_object_id(bussinessid)
        bussiness.delete()
        if self.get_object_id(bussinessid):
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


class SetBussiness(APIView):

    def get_object_id(self, id):
        try:
            return Bussiness.objects.filter(id=id)
        except Exception as e:
            logger.error(e)

    def update_detail(self, object, name, operatorid, productorid):
        try:
            return object.update(name=name, operatorid=operatorid, productorid=productorid)
        except Exception as e:
            logger.error(e)

    def post(self, request, format=None):

        bussinessid = json.loads(request.body).get('bussinessid', None)
        if bussinessid is None:
            raise ParamException('bussinessid')
        name = json.loads(request.body).get('name', None)
        operatorid = json.loads(request.body).get('operatorid', None)
        productorid = json.loads(request.body).get('productorid', None)

        bussiness = self.get_object_id(bussinessid)
        if bussiness:
            update = self.update_detail(bussiness, name, operatorid, productorid)
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
            return Response(msg)


class BussinessModuleServer(APIView):

    def post(self, request, format=None):

        bussinessid = json.loads(request.body).get('bussinessid', None)
        moduleid = json.loads(request.body).get('moduleid', None)
        clusterid = json.loads(request.body).get('clusterid', None)
