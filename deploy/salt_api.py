#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import urllib
import urllib2
import json
import ssl

class SaltAPI(object):
    __token_id = ''
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.header = {'Accept': 'application/x-yaml'}

    def token_id(self):
        params = {
            'username': self.username,
            'password': self.password,
            'eauth': 'pam'
        }
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        content = self.postRequest(obj,prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def postRequest(self,obj,prefix='/'):
        url = self.url + prefix
        context = ssl._create_unverified_context()
        headers = {'X-Auth-Token'   : self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req, context=context)
        content = json.loads(opener.read())
        return content

    def remote_execute(self, tgt, fun, arg, expr_form='glob'):
        params = {
            'client': 'local',
            'tgt': tgt,
            'fun': fun,
            'arg': arg,
            'expr_form': expr_form
        }
        obj = urllib.urlencode(params)
        self.token_id() # 重新获取一次token
        content = self.postRequest(obj)
        ret = content['return']
        # print ret
        return ret

    def list_all_key(self):
        '''
        获取包括认证、未认证salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions,minions_pre

    def delete_key(self,node_name):
        '''
        拒绝salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def accept_key(self,node_name):
        '''
        接受salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def salt_runner(self,jid):
        '''
        通过jid获取执行结果
        '''

        params = {'client':'runner', 'fun':'jobs.lookup_jid', 'jid': jid}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def salt_running_jobs(self):
        '''
        获取运行中的任务
        '''

        params = {'client':'runner', 'fun':'jobs.active'}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def salt_state(self,tgt,arg,expr_form):
        '''
        sls文件
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': expr_form}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret


    def project_manage(self,tgt,fun,arg1,arg2,arg3,arg4,arg5,expr_form):
        '''
        文件上传、备份到minion、项目管理
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        # 拼接url参数
        params2 = {'arg':arg2}
        arg_add = urllib.urlencode(params2)
        obj = urllib.urlencode(params)
        obj = obj + '&' + arg_add
        params3 = {'arg': arg3}
        arg_add = urllib.urlencode(params3)
        obj = obj + '&' + arg_add
        params4 = {'arg': arg4}
        arg_add = urllib.urlencode(params4)
        obj = obj + '&' + arg_add
        params5 = {'arg': arg5}
        arg_add = urllib.urlencode(params5)
        obj = obj + '&' + arg_add
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def file_copy(self,tgt,fun,arg1,arg2,expr_form):
        '''
        文件上传、备份到minion、项目管理
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        # 拼接url参数
        params2 = {'arg':arg2}
        arg_add = urllib.urlencode(params2)
        obj = urllib.urlencode(params)
        obj = obj + '&' + arg_add
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def file_bak(self, tgt, fun, arg, expr_form):
        '''
        文件备份到master
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def file_manage(self, tgt, fun, arg1, arg2, arg3, expr_form):
        '''
        文件回滚
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        params2 = {'arg': arg2}
        arg_add = urllib.urlencode(params2)
        obj = urllib.urlencode(params)
        obj = obj + '&' + arg_add
        params3 = {'arg': arg3}
        arg_add_2 = urllib.urlencode(params3)
        obj = obj + '&' + arg_add_2
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def remote_server_info(self, tgt, fun):
        '''
        获取远程主机信息
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

if __name__ == '__main__':
    url = 'https://112.74.164.242:7000'
    test = SaltAPI(url, 'saltapi', 'saltadmin')
    test.remote_execute('web_test_1001', 'cmd.run', 'python /apps/sh/node_init.py YoungBody init', 'glob')
