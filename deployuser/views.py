# coding: utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .user_api import *
from .form import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

import datetime
import json

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = json.loads(request.body)[u'username']
        password = json.loads(request.body)[u'password']
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
                    'retmsg': '登录成功'
                }
                # print data
                return HttpResponse(json.dumps(data))
            else:
                msg = {
                    'retcode': 1,
                    'retmsg': 'Not a valid user'
                }
                return HttpResponse(json.dumps(msg))
        else:
            HttpResponse("{'retmsg': 'Wrong username or password!'}")
    return HttpResponse("{'retmsg': 'Null'}")
