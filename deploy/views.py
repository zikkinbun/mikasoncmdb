# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from .models import deployRecord
# Create your views here.

from .gitlab_api import *
from .salt_api import *

import time
import subprocess
import shutil
import json
import os

node_project_list = ['platformService', 'uco2Web', 'gdrManagerSystem', 'uco2Notice', 'YoungBody', 'kalachakraWeb', 'kalachakraService']
php_project_list = ['beeHive', 'uco2H5', 'kalachakraMS']

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
        tarfile_path = os.path.join(package_path, 'releases')
        project_dir = os.path.join(package_path, project)
        saltmaster_dir = '/srv/salt/test/packages/'

        url = get_url_api(project)
        reurl = str(url).replace('192.168.1.3', '112.74.182.80')
        dirname = project + '_test_' + branch + '_' + tag
        filename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d")
        tarfilename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
        # 先在master上处理git操作
        if branch != 'master':
            lcd = os.chdir(package_path)
            arg = 'git clone ' + reurl
            clone = subprocess.Popen(arg)
            if os.path.exists(project_dir):
                os.chdir(project_dir)
                arg = 'git checkout -b ' + branch + ' origin/' + branch
                checkout = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
                return HttpResponse(checkout.stdout)
            else:
                msg = clone.stdout
                return HttpResponse(msg)
        else:
            lcd = os.chdir(package_path)
            # pwd = os.getcwd()
            arg = 'git clone ' + reurl
            clone = os.popen(arg).readlines()
            # print clone

        # print os.listdir(package_path)
        # print os.path.exists(project_dir)
        # 在master上打包
        if os.path.exists(project_dir):
            shutil.move(project_dir, project_dir + '_test_' + branch + '_' + tag)
            tag_dir = project_dir + '_test_' + branch + '_' + tag
            if os.path.exists(tag_dir):
                os.chdir(tarfile_path)
                shutil.make_archive(filename, "gztar", root_dir=tag_dir)
                msg = {
                    'retcode': '0',
                    'retmsg': 'tar dir success'
                }
                # return HttpResponse(json.dumps(msg))
            else:
                msg = {
                    'retcode': '-1',
                    'retmsg': 'The project dir is not exists'
                    }
                return HttpResponseServerError(json.dumps(msg))
        else:
            msg = {
                'retcode': '-2',
                'retmsg': 'The filedir is not exists'
            }
            return HttpResponseServerError(json.dumps(msg))

        # 转移到master的上传目录复制到minions上
        # print tarfile_path + tarfilename
        # print os.path.exists(tarfile_path + '/' + tarfilename)
        if os.path.exists(tarfile_path + '/' + tarfilename):
            shutil.copyfile(tarfile_path + '/' + tarfilename, saltmaster_dir + tarfilename)
        else:
            msg = 'copy error'
            return HttpResponseServerError(json.dumps(msg))

        # 使用saltapi上传文件并进行初始化
        if os.path.exists(saltmaster_dir + tarfilename):
            saltapi = SaltAPI('https://112.74.164.242:7000', 'saltapi', 'saltadmin')
            src = 'salt://test/packages/' + tarfilename
            dst = '/home/wwwroot/releases/' + tarfilename
            upload = saltapi.file_copy(test_host, 'cp.get_file', src, dst, 'glob')
            if upload:
                mk = 'mkdir -p ' + '/home/wwwroot/releases/' + filename
                mkdir = saltapi.remote_execute(test_host, 'cmd.run', mk, 'glob')
                tar = 'tar zxvf ' + dst + ' -C /home/wwwroot/releases/' + filename
                untar = saltapi.remote_execute(test_host, 'cmd.run', tar, 'glob')
                rm = 'rm -rf /home/wwwroot/current/' + project
                remove = saltapi.remote_execute(test_host, 'cmd.run', rm, 'glob')
                ln = 'ln -s /home/wwwroot/releases/' + filename + ' /home/wwwroot/current/' + project
                softlink = saltapi.remote_execute(test_host, 'cmd.run', ln, 'glob')
                # update config and reload project
                if project in node_project_list:
                    rm, link = init_node_project_config(project, '/home/wwwroot/releases/' + filename)
                    init = 'python /apps/sh/node_init.py %s init' % project
                    rm_run = saltapi.remote_execute(test_host, 'cmd.run', rm, 'glob')
                    link_run = saltapi.remote_execute(test_host, 'cmd.run', link, 'glob')
                    init_run = saltapi.remote_execute(test_host, 'cmd.run', init, 'glob')
                    record = deployRecord.objects.create(project_name=project, project_owner='node', deploy_branch=branch, deploy_tag=tag)
                    msg = {
                        'retcode': 3,
                        'retdata': project + ' deploy testing successfully',
                    }
                    return HttpResponse(json.dumps(msg))
                elif project in php_project_list:
                    rm, rm_next, link, link_next = init_php_project_config(project, '/home/wwwroot/releases/' + filename)
                    rm_run = saltapi.remote_execute(test_host, 'cmd.run', rm, 'glob')
                    rm_next_run = saltapi.remote_execute(test_host, 'cmd.run', rm_next, 'glob')
                    link_run = saltapi.remote_execute(test_host, 'cmd.run', link, 'glob')
                    link_next_run = saltapi.remote_execute(test_host, 'cmd.run', link_next, 'glob')
                    record = deployRecord.objects.create(project_name=project, project_owner='php', deploy_branch=branch, deploy_tag=tag)
                    msg = {
                        'retcode': 3,
                        'retdata': project + ' deploy testing successfully',
                    }
                    return HttpResponse(json.dumps(msg))
                else:
                    msg = {
                        'retdata': 'current path is not exist'
                    }
                return HttpResponseServerError(json.dumps(msg))
            else:
                msg = 'upload failed'
                return HttpResponseServerError(json.dumps(msg))
        else:
            msg = 'saltfile error'
            return HttpResponseServerError(json.dumps(msg))

def init_php_project_config(project, path):
    php_project_list = ['beeHive', 'uco2H5', 'kalachakraMS']
    if project in node_project_list:
        test_path = path + '/Global/config.test.js'
        cur_path = path + '/Global/config.js'
        test_path_next = path + '/Interface/application/config.test.php'
        cur_path_next = path + '/Interface/application/config.php'
        rm = 'rm -f ' + cur_path
        rm_next = 'rm -f ' + cur_path_next
        link = 'ln -s ' + test_path + ' ' + cur_path
        link_next = 'ln -s ' + test_path_next + ' ' + cur_path_next
        return rm, rm_next, link, link_next
    else:
        msg = {
            'retcode': 1
        }
        return msg

def init_node_project_config(project, path):
    node_project_list = ['platformService', 'uco2Web', 'gdrManagerSystem', 'uco2Notice', 'YoungBody', 'kalachakraWeb', 'kalachakraService']
    if project in node_project_list:
        test_path = path + '/global/config.test.js'
        cur_path = path + '/global/config.js'
        rm = 'rm -f ' + cur_path
        link = 'ln -s ' + test_path + ' ' + cur_path
        return rm, link
    else:
        msg = {
            'retcode': 1
        }
        return msg
