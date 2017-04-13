#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .models import *
from .gitlab_api import *

from fabric.api import *
from fabric.main import main
from fabric.contrib import django
import os
import time

env.roledefs = {
    # 'web_prod': ['112.74.15.176', '112.74.19.19', '112.74.24.16', '120.24.253.130', '120.24.247.230'],
    # 'db_prod': ['112.74.195.114', '112.74.195.0'],
    # 'web_stage': ['112.74.27.20 ', '120.25.106.206'],
    'web_test': ['192.168.1.1'],
    'web_prod': ['192.168.1.6']
}

# env.user = 'apps'
env.user = 'root'
# env.hosts = ['120.24.247.230', '112.74.15.176']
env.password = ')2`@)2Hd5EQx'  # 测试

# env.port = '2222'
env.port = '22'

env.project_dev_source = '/apps/packages/'
env.project_start_shell = '/apps/sh/'
env.project_tar_source = '/apps/packages/releases/'

env.deploy_project_root = '/home/wwwroot/'
env.deploy_release_dir = 'releases/'
env.deploy_current_dir = 'current/'

class Deploy(object):
    def __init__(self, project_name, branch, tag):
        self.project_name = project_name
        self.branch = branch
        self.tag = tag

    def tar_pack(self, action):
        if action == '新建版本':
            path = env.project_dev_source + self.project_name
            url = self.get_url(self.project_name)
            if os.path.exists(path):
                local("rm -rf %s" % path)
                local("sudo git clone %s" % url)
                with lcd(env.project_dev_source):
                    local("mv %s %s" % (self.project_name, self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag)))
                    local("tar -zcvf %s.tar.gz %s" % (env.project_tar_source + self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag) + '_' + time.strftime("%Y%m%d"), self.project_name + '_' + 'test_' + self.branch + '_' + (self.tag)))
            else:
                local("sudo git clone %s" % url)
        elif action == '发布标签版本':
            path = env.project_dev_source + (self.project_name + '_' + 'test_' + self.branch + '_' + self.tag)
            if os.path.exists(path):
                if branch == 'master':
                    with lcd(path):
                        local("sudo git checkout -b master %s" % self.tag)
                        local("mv %s %s" % (self.project_name, self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag)))
                        local("tar -zcvf %s.tar.gz %s" % (env.project_tar_source + self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag) + '_' + time.strftime("%Y%m%d"), self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag)))
                else:
                    project_branch_list = get_branches(self.project_name)
                    if branch in project_branch_list:
                        with lcd(path):
                            local("sudo git checkout -b %s origin/%s" % (self.branch, self.branch))
                            local("sudo git checkout -b %s %s" % (self.branch, tag))
                        with lcd(env.project_dev_source):
                            local("mv %s %s" % (self.project_name, self.project_name + '_' + 'test_' + self.branch + '_' + str(tag)))
                            local("tar -zcvf %s.tar.gz %s" % (env.project_tar_source + self.project_name + '_' + 'test_' + self.branch + '_' + str(tag) + '_' + time.strftime("%Y%m%d"), self.project_name + '_' + 'test_' + self.branch + '_' + str(tag)))
            else:
                with lcd(env.project_dev_source):
                    local("sudo git clone %s" % url)
                with lcd(path):
                    local("sudo git checkout -b %s origin/%s" % (self.branch, self.branch))
                    local("sudo git checkout -b %s %s" % (self.branch, tag))
                with lcd(env.project_dev_source):
                    local("mv %s %s" % (self.project_name, self.project_name + '_' + 'test_' + self.branch + '_' + str(tag)))
                    local("tar -zcvf %s.tar.gz %s" % (env.project_tar_source + self.project_name + '_' + 'test_' + self.branch + '_' + str(tag) + '_' + time.strftime("%Y%m%d"), self.project_name + '_' + 'test_' + self.branch + '_' + str(tag)))
        elif action == '发布分支版本':
            path = env.project_dev_source + (self.project_name + '_' + 'test_' + self.branch + '_' + tag)
            if os.path.exists(path):
                if self.branch != 'master' and branch in project_branch_list:
                    with lcd(path):
                        local("sudo git checkout -D %s" % self.branch)
                        local("sudo git checkout -b %s origin/%s" % (self.branch, self.branch))
                    with lcd(env.project_dev_source):
                        local("mv %s %s" % (self.project_name, self.project_name + '_' + 'test_' + self.branch + '_' + str(tag)))
                        local("tar -zcvf %s.tar.gz %s" % (env.project_tar_source + self.project_name + '_' + 'test_' + self.branch + '_' + str(tag) + '_' + time.strftime("%Y%m%d"), self.project_name + '_' + 'test_' + self.branch + '_' + str(tag)))
                elif self.branch == 'master':
                    with lcd(path):
                        local("sudo git pull origin master")
                    with lcd(env.project_dev_source):
                        local("mv %s %s" % (self.project_name, self.project_name + '_' + 'test_' + self.branch + '_' + str(tag)))
                        local("tar -zcvf %s.tar.gz %s" % (env.project_tar_source + self.project_name + '_' + 'test_' + self.branch + '_' + str(tag) + '_' + time.strftime("%Y%m%d"), self.project_name + '_' + 'test_' + self.branch + '_' + str(tag)))
                else:
                    return 'error branch'
        else:
            return 'error release function'

        def put_pack(self):
            tar_path = env.project_tar_source + self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag) + '_' + time.strftime("%Y%m%d")
            with settings(warn_only=True):
                result = put(tar_path, env.deploy_project_root + env.deploy_release_dir)
                if result.failed:
                    abort("abort file task")
            with cd(env.deploy_full_path):
                run("tar -zxvf %s.tar.gz" % (
                    self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag) + '_' + time.strftime("%Y%m%d")))
                run("rm -rf %s.tar.gz" % (self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag) + '_' + time.strftime("%Y%m%d")))
                print "package success!"

        def update_configfile(self):
            node_projects = ('platformService', 'uco2Web', 'gdrManagerSystem', 'uco2Notice', 'kalachakraService', 'kalachakraWeb')
            php_projects = ('beeHive', 'uco2H5', 'kalachakraMS', 'gdrOffcial')
            config_path = env.deploy_project_root + env.deploy_release_dir + self.project_name + '_' + 'test_' + self.branch + '_' + str(self.tag) + '_' + time.strftime("%Y%m%d")
            if project in node_projects:
                node_test_configfile = config_path + '/global/config.test.js'
                node_configfile = config_path + '/global/config.js'
                with settings(warn_only=True):
                    run("rm -f %s" % node_configfile)
                    run("ln -s %s %s" % (node_test_configfile, node_configfile))
            elif project in php_projects:
                php_test_configfile_1 = config_path + '/Global/config.test.js'
                php_test_configfile_2 = config_path + '/Interface/application/config.test.php'
                php_configfile_1 = config_path + '/Global/config.js'
                php_configfile_2 = config_path + '/Interface/application/config.php'
                with settings(warn_only=True):
                    run("rm -f %s" % php_configfile_1)
                    run("rm -f %s" % php_configfile_2)
                    run("ln -s %s %s" % (php_test_configfile_1, php_configfile_1))
                    run("ln -s %s %s" % (php_test_configfile_2, php_configfile_2))
            else:
                return 'error configfile'

        def make_symlink(self):
            env.deploy_full_path = env.deploy_project_root + \
                env.deploy_release_dir + self.project + '_' + 'test_' + self.branch + '_' + str(self.tag) + '_' + time.strftime("%Y%m%d")
            with settings(warn_only=True):
                run("rm -rf %s" % (env.deploy_project_root +
                                   env.deploy_current_dir + self.project))
                run("ln -s %s %s" % (env.deploy_full_path,
                                     env.deploy_project_root + env.deploy_current_dir + self.project))
                run("chown -R apps.apps %s" % env.deploy_full_path)
