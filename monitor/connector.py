# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import pymysql

class mysql_connector(object):

    def __init__(self, host, port, user, password, db=None, charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    # 建立连接
    def get_con(self):
        try:
            conn = pymysql.connect(host=self.host, user=self.user, passwd=self.password, db=self.db, port=self.port, charset=self.charset)
            return conn
        except pymysql.Error, e:
            print "pymysql Error:%s" % e

    # 查询方法，使用con.cursor(MySQLdb.cursors.DictCursor),返回结果为字典
    def select_all(self, sql):
        try:
            con = self.get_con()
            cur = con.cursor(pymysql.cursors.DictCursor)
            count = cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except pymysql.Error, e:
            print "pymysql Error:%s" % e
        finally:
            cur.close()
            con.close()

    def select_by_where(self, sql, data):
        try:
            con = self.get_con()
            d = (data,)
            cur = con.cursor(pymysql.cursors.DictCursor)
            count = cur.execute(sql, d)
            fc = cur.fetchall()
            # if len(fc) > 0:
            #     for e in range(len(fc)):
            #         print(fc[e])
            return fc
        except pymysql.Error, e:
            print "pymysql Error:%s" % e
        finally:
            cur.close()
            con.close()

    # 带参数的更新方法,eg:sql='insert into pythontest values(%s,%s,%s,now()',params=(6,'C#','good book')
    def dml_by_where(self, sql, params):
        try:
            con = self.get_con()
            cur = con.cursor()

            for d in params:
                if self.SHOW_SQL:
                    print('执行sql:[{}],参数:[{}]'.format(sql, d))
                cur.execute(sql, d)
            con.commit()

        except pymysql.Error, e:
            con.rollback()
            print "pymysql Error:%s" % e
        finally:
            cur.close()
            con.close()

    # 不带参数的更新方法
    def dml_nowhere(self, sql):
        try:
            con = self.get_con()
            cur = con.cursor()
            count = cur.execute(sql)
            con.commit()
            return count
        except pymysql.Error,e:
            con.rollback()
            print "pymysql Error:%s" % e
        finally:
            cur.close()
            con.close()
