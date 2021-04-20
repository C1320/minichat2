#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/2/1 15:07
# @Author : 十三
# @Email : 2429120006@qq.com
# @Site : 
# @File : remenber_sql.py
# @Software: PyCharm
import pymysql


class reb_sql():
    def __init__(self):
        self.list = []

    def find_sql(self):
        # 打开数据库
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='mysql', charset='utf8')
        # 获取操作游标
        self.cur = self.conn.cursor()
        # 执行SQL语句
        try:
            self.cur.execute("select*from remember")
            #     fetchall查询全部结果   fetchone查询单条数据
            self.result = self.cur.fetchall()
            for row in self.result:
                self.list.append(row[0])
            return self.list
        except Exception as e:
            # 抛出异常
            print("异常", e)
        finally:
            self.conn.close()
    '''
    记住账号密码
    '''
    def insert_sql(self, account,name):
        lt = []
        self.username = []
        # 打开数据库
        self.insert_conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='mysql',
                                           charset='utf8')
        # 获取操作游标
        self.insert_cur = self.insert_conn.cursor()
        # 执行SQL语句
        try:
            self.insert_cur.execute("select*from remember")
            result = self.insert_cur.fetchall()
            for row in result:
                lt.append(row[0])
            if account not in lt:
                self.insert_account = "insert into remember(ID,name)values ('%s','%s')" % (account,name)
                self.insert_cur.execute(self.insert_account)
                self.insert_conn.commit()
        except Exception as e:
            # 抛出异常
            print("异常", e)
        finally:
            self.insert_conn.close()
