# coding: utf-8

import time
import subprocess
import shutil
import json
import os

from .salt_api import *
from .gitlab_api import *

from .models import deployRecord

class deployOper:

    def __init__(self, host, project, branch, tag):
        self.host = host
        self.project = project
        self.branch = branch
        self.tag = tag
        self.node_project_list = ['platformService', 'uco2Web', 'gdrManagerSystem', 'uco2Notice', 'YoungBody', 'kalachakraWeb', 'kalachakraService']
        self.php_project_list = ['beeHive', 'uco2H5', 'kalachakraMS']
        self.package_path = '/apps/packages/'
        self.saltmaster_dir = '/srv/salt/test/packages/'
        self.tarfile_path = os.path.join(package_path, 'releases')
        self.project_dir = os.path.join(package_path, project)
        self.dirname = self.project + '_test_' + self.branch + '_' + self.tag
        self.filename = self.project + '_test_' + self.branch + '_' + self.tag + '_' + time.strftime("%Y%m%d")
        self.tarfilename = self.project + '_test_' + self.branch + '_' + self.tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
        self.src = 'salt://test/packages/' + self.tarfilename
        self.dst = '/home/wwwroot/releases/' + self.tarfilename

    def git_oper(self):
        url = get_url_api(self.project)
        # 基于分支checkout
        if branch != 'master':
            lcd = os.chdir(self.package_path)
            arg = 'git clone ' + url
            clone = os.popen(arg).readlines()
            if os.path.exists(self.project_dir):
                os.chdir(self.project_dir)
                arg = 'git checkout -b ' + branch + ' origin/' + branch
                checkout = os.popen(arg)
                msg = {
                    'retcode': 0,
                    'retdata': branch
                    'retmsg': '目录创建成功'
                }
                return msg
            else:
                msg = clone
                return msg
        else:
            lcd = os.chdir(self.package_path)
            arg = 'git clone ' + url
            clone = os.popen(arg).readlines()
            msg = {
                'retcode': 0,
                'retdata': branch
                'retmsg': '目录创建成功'
            }
            return msg

    def move_oper(self):
        if os.path.exists(self.project_dir):
            shutil.move(self.project_dir, self.project_dir + '_test_' + self.branch + '_' + self.tag)
            tag_dir = self.project_dir + '_test_' + self.branch + '_' + self.tag
            if os.path.exists(tag_dir):
                os.chdir(self.tarfile_path)
                shutil.make_archive(self.filename, "gztar", root_dir=tag_dir)
                msg = {
                    'retcode': 0,
                    'retmsg': '目录打包成功'
                }
                return msg
            else:
                msg = {
                    'retcode': -1,
                    'retmsg': 'tar目录不存在'
                    }
                return msg
        else:
            msg = {
                'retcode': -2,
                'retmsg': '项目路径不存在'
            }
            return msg

    def tar_oper(self):
        if os.path.exists(self.tarfile_path + '/' + self.tarfilename):
            shutil.copyfile(self.tarfile_path + '/' + self.tarfilename, self.saltmaster_dir + self.tarfilename)
            msg = {
                'retcode': 0,
                'retmsg': '项目打包成功并复制到上传目录待命'
            }
            return msg
        else:
            msg = {
                'retcode': -1,
                'retmsg': '项目打包失败'
            }
            return msg

    def upload_oper(self):
        if os.path.exists(self.saltmaster_dir + self.tarfilename):
            saltapi = SaltAPI('https://112.74.164.242:7000', 'saltapi', 'saltadmin')
            self.src = 'salt://test/packages/' + self.tarfilename
            dst = '/home/wwwroot/releases/' + self.tarfilename
            ft_rm = 'rm -rf /home/wwwroot/releases/' + self.filename
            rm_ft = saltapi.remote_execute(self.host, 'cmd.run', ft_rm, 'glob')
            tar_rm = 'rm -rf /home/wwwroot/releases/' + self.tarfilename
            rm_tar = saltapi.remote_execute(self.host, 'cmd.run', tar_rm, 'glob')
            upload = saltapi.file_copy(test_host, 'cp.get_file', self.src, self.dst, 'glob')
            if upload:
                msg = {
                    'retcode': 0,
                    'retmsg': '上传成功'
                }
                return mgs
            else:
                msg = {
                    'retcode': -1,
                    'retmsg': '上传失败'
                }
                return mgs
        else:
            msg = {
                'retcode': -1,
                'retmsg': '源文件不存在请检查'
            }

    def config_oper(self):
        srv_arg = 'rm -rf ' + self.saltmaster_dir + self.tarfilename
        rm_srv = os.popen(srv_arg)
        # print rm_srv
        tar_arg = 'rm -rf ' + self.tarfile_path + '/' + self.tarfilename
        rm_tar = os.popen(tar_arg)
        # print rm_tar
        folder_arg = 'rm -rf ' + self.package_path + self.dirname
        rm_folder = os.popen(folder_arg)
        # print rm_folder
        mk = 'mkdir -p ' + '/home/wwwroot/releases/' + self.filename
        mkdir = saltapi.remote_execute(self.host, 'cmd.run', mk, 'glob')
        tar = 'tar zxvf ' + self.dst + ' -C /home/wwwroot/releases/' + self.filename
        untar = saltapi.remote_execute(self.host, 'cmd.run', tar, 'glob')
        rm = 'rm -rf /home/wwwroot/current/' + self.project
        remove = saltapi.remote_execute(self.host, 'cmd.run', rm, 'glob')
        ln = 'ln -s /home/wwwroot/releases/' + filename + ' /home/wwwroot/current/' + self.project
        softlink = saltapi.remote_execute(self.host, 'cmd.run', ln, 'glob')

    def init_php_project_config(self, path, env):
        # php_project_list = ['beeHive', 'uco2H5', 'kalachakraMS']
        if self.project in self.php_project_list:
            if env == 'test':
                test_path = path + '/Global/config.test.js'
                cur_path = path + '/Global/config.js'
                test_path_next = path + '/Interface/application/config.test.php'
                cur_path_next = path + '/Interface/application/config.php'
                rm = 'rm -f ' + cur_path
                rm_next = 'rm -f ' + cur_path_next
                link = 'ln -s ' + test_path + ' ' + cur_path
                link_next = 'ln -s ' + test_path_next + ' ' + cur_path_next
                return rm, rm_next, link, link_next
            elif env == 'prod':
                prod_path = path + '/Global/config.prod.js'
                cur_path = path + '/Global/config.js'
                prod_path_next = path + '/Interface/application/config.prod.php'
                cur_path_next = path + '/Interface/application/config.php'
                rm = 'rm -f ' + cur_path
                rm_next = 'rm -f ' + cur_path_next
                link = 'ln -s ' + prod_path + ' ' + cur_path
                link_next = 'ln -s ' + prod_path_next + ' ' + cur_path_next
                return rm, rm_next, link, link_next
            else:
                msg = {
                    'retcode': -1
                    }
                return msg
        else:
            msg = {
                'retcode': 1
            }
            return msg

    def init_node_project_config(self, path, env):
        # node_project_list = ['platformService', 'uco2Web', 'gdrManagerSystem', 'uco2Notice', 'YoungBody', 'kalachakraWeb', 'kalachakraService']
        if self.project in self.node_project_list:
            if env == 'test':
                test_path = path + '/global/config.test.js'
                cur_path = path + '/global/config.js'
                rm = 'rm -f ' + cur_path
                link = 'ln -s ' + test_path + ' ' + cur_path
                return rm, link
            elif env == 'prod':
                prod_path = path + '/global/config.prod.js'
                cur_path = path + '/global/config.js'
                rm = 'rm -f ' + cur_path
                link = 'ln -s ' + prod_path + ' ' + cur_path
                return rm, link
            else:
                msg = {
                    'retcode': -1
                }
                return msg
        else:
            msg = {
                'retcode': 1
            }
            return msg

    def file_oper(self):
        if self.project in self.node_project_list:
            rm, link = self.init_node_project_config('/home/wwwroot/releases/' + self.filename, 'test')
            rm_run = saltapi.remote_execute(self.host, 'cmd.run', rm, 'glob')
            link_run = saltapi.remote_execute(self.host, 'cmd.run', link, 'glob')
            chown = 'chown -R prod.prod /home/wwwroot/releases/' + self.filename
            chown_run = saltapi.remote_execute(self.host, 'cmd.run', chown, 'glob')
            msg = {
                'retcode': 0,
                'retmsg': '运行目录创建成功'
            }
            return msg
        elif self.project in self.php_project_list:
            rm, rm_next, link, link_next = self.init_php_project_config('/home/wwwroot/releases/' + self.filename, 'test')
            rm_run = saltapi.remote_execute(self.host, 'cmd.run', rm, 'glob')
            rm_next_run = saltapi.remote_execute(self.host, 'cmd.run', rm_next, 'glob')
            link_run = saltapi.remote_execute(self.host, 'cmd.run', link, 'glob')
            link_next_run = saltapi.remote_execute(self.host, 'cmd.run', link_next, 'glob')
            chown = 'chown -R prod.prod /home/wwwroot/releases/' + self.filename
            chown_run = saltapi.remote_execute(self.host, 'cmd.run', chown, 'glob')
            msg = {
                'retcode': 0,
                'retmsg': '运行目录创建成功'
            }
            return msg
        else:
            msg = {
                'retcode': -1,
                'retmsg': '运行目录创建失败'
            }
            return msg

    def service_oper(self):
        if self.project in self.node_project_list:
            init = 'python /apps/sh/node_init.py %s init' % self.project
            init_run = saltapi.remote_execute(self.host, 'cmd.run', init, 'glob')
            record = deployRecord.objects.create(project_name=self.project, project_owner='node', deploy_branch=self.branch, deploy_tag=self.tag)
        elif project in php_project_list:
            record = deployRecord.objects.create(project_name=self.project, project_owner='php', deploy_branch=self.branch, deploy_tag=self.tag)
