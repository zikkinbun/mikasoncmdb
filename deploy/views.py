# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from .gitlab_api import *
from .salt_api import *

import time
import subprocess
import shutil
import json
import os

@csrf_exempt
def pushTest(request):
    if request.POST:
        project = json.loads(request.body)[u'project']
        branch = json.loads(request.body)[u'branch']
        tag = json.loads(request.body)[u'tag']
        # project = request.POST.get('project', '')
        # branch = request.POST.get('branch', '')
        # tag = request.POST.get('tag', '')

        test_host = 'web_test_1001'
        package_path = '/apps/packages/'
        tarfile_path = os.path.join(package_path, 'release')
        project_dir = os.path.join(package_path, project)
        saltmaster_dir = '/srv/salt/test/packages/'

        url = get_url_api(project)
        dirname = project + '_test_' + branch + '_' + tag
        filename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d")
        tarfilename = project + '_test_' + branch + '_' + tag + '_' + ttime.strftime("%Y%m%d") + '.tar.gz'
        # 先在master上处理git操作
        if branch != 'master':
            lcd = os.chdir(package_path)
            clone = subprocess.PIPE('git clone %s', shell=True, stdout=subprocess.PIPE) % url
            if os.path.exists(project_dir):
                os.chdir(project_dir)
                checkout = subprocess.Popen('git checkout -b %s origin/%s', shell=True, stdout=subprocess.PIPE) % (branch, branch)
                return checkout.stdout
            else:
                msg = clone.stdout
                return msg
        else:
            lcd = os.chdir(package_path)
            clone = subprocess.PIPE('git clone %s', shell=True, stdout=subprocess.PIPE) % url
        # 在master上打包
        if os.path.exists(project_dir):
            tag_dir = shutil.move(project_dir, project_dir + '_test_' + branch + '_' + tag)
            if os.path.exists(tag_dir):
                os.chdir(tarfile_path)
                shutil.make_archive(filename, "tar.gz", root_dir=project_dir)
            else:
                msg = 'The project dir is not exists'
                return msg
        else:
            msg = 'The filedir is not exists'
            return msg

        # 转移到master的上传目录复制到minions上
        if os.path.exists(tarfile_path + filename):
            shutil.copyfile(tarfile_path + filename, saltmaster_dir + filename)
        else:
            msg = 'copy error'
            return msg

        # 使用saltapi上传文件
        saltapi = SaltAPI('https://127.0.0.1:7000', 'saltapi', 'saltadmin')
        upload = saltapi.file_copy(test_host, 'cp.get_file', 'salt://test/packages/%s', '/home/wwwroot/release/%s') % (filename, filename)
        return upload
