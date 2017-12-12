# coding: utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserSerializer

import os
import json
import datetime
import binascii
import hashlib


class CreateAccount(APIView):

    def _set_password(self, username, password):
        user = CustomUser.objects.get(username=username)
        user.set_password(password)
        user.save()

    def post(self, request, format=None):
        username = json.loads(request.body).get('username', None)
        if username is None:
            raise ParamException('username')
        password = json.loads(request.body).get('password', None)
        if password is None:
            raise ParamException('password')
        email = json.loads(request.body).get('email', None)
        if email is None:
            raise ParamException('email')
        phone = json.loads(request.body).get('phone', None)
        if phone is None:
            raise ParamException('phone')
        staff = json.loads(request.body).get('staff', None)
        if staff is None:
            raise ParamException('staff')

        user = {
            'username': username,
            'password': password,
            'email': email,
            'phone': phone,
            'staff': staff
        }

        serializer = CustomUserSerializer(data=user)
        if serializer.is_valid():
            serializer.save()
            self._set_password(username, password)
            data = serializer.data
            msg = {
                'retcode': 0,
                'retdata': data,
                'retmsg': 'add user success'
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAccount(APIView):

    def post(self, request, format=None):
        username = json.loads(request.body).get('username', None)
        if username is None:
            raise ParamException('username')
        password = json.loads(request.body).get('password', None)
        if password is None:
            raise ParamException('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                data = {
                    'retcode': 0,
                    'retdata': {
                        'id': user.id,
                        'name': user.username,
                        'mail': user.email,
                        'active': user.is_active
                    },
                    'retmsg': 'login success'
                }
                return Response(data)
            else:
                data = {
                    'retcode': -1,
                    'retmsg': 'the user is not actived'
                }
                return Response(data)
        else:
            data = {
                'retcode': -1,
                'retmsg': 'username or password is wrong'
            }
            return Response(data)


class GetAccountAll(APIView):

    def get_user_object(self):
        try:
            users = CustomUser.objects.all()
            datas = []
            for user in users:
                data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone
                }
                datas.append(data)
            return datas
        except Exception as e:
            print e

    def get_user_by_id(self, id):
        try:
            users = CustomUser.objects.get(id=id)
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
        userid = json.loads(request.body).get('userid', None)

        if userid:
            data = self.get_user_by_id(userid)
            msg = {
                'retcode': 0,
                'retdata': data
            }
            return Response(msg)
        else:
            data = self.get_user_object()
            msg = {
                'retcode': 0,
                'retdata': data
            }
            return Response(msg)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'retcode': 0,
        'retdata': {
            'token': token,
            'user': CustomUserSerializer(user).data
        }
    }
