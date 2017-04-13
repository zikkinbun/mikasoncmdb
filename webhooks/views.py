#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
import os
# Create your views here.
@csrf_exempt
def index(request, *args, **kwargs):
    if request.method == 'POST' and json.loads(request.body)[u'object_kind'] == 'push':
        try:
            # return HttpResponse(request.body)
            # return render(request, 'gitweb/index.html', content_type='application/json')
            json_data = json.loads(request.body)
            # print json_data[u'project_id']
            ref = json_data[u'ref']
            if not ref:
                return HttpResponse('Invalid branch')
            # branch = str(ref).split('/')[2]
            branch = 'master'
            project_name = json_data[u'project'][u'name']
            if not project_name:
                return HttpResponse('Invalid project')
            url = json_data[u'repository'][u'url']
            if not url:
                return HttpResponse('Invalid url')
            path = '/apps/project/' + project_name
            os.chdir(path)
            os.popen('git pull origin master')
            if project_name == 'beeHive':
                os.popen('/etc/init.d/nginx restart')
            elif project_name == 'platformService' or project_name == 'uco2Web':
                os.popen('/apps/sh/node_start.sh restart_%s' % project_name)
            else:
                os.popen('/etc/init.d/nginx restart')
                os.popen('/etc/init.d/php-fpm restart')
            # history = subprocess.Popen(['git', 'log'], stdout=subprocess.PIPE)
            print ("Done [git pull origin %s]") % branch
            return HttpResponse('ok!')
        except:
            raise Http404('Can not find the page')
