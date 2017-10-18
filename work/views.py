# _*_ coding:utf-8_*_
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

import json

class DBInsertUser(APIView):

    def post(self):

        env = json.loads(request.body).get('env', None)
        username = json.loads(request.body).get('username', None)
