#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/1/30 20:02
# @Author : 十三
# @Email : 2429120006@qq.com
# @Site : 
# @File : cyq_sql.py
# @Software: PyCharm
import pymysql


class L_sql():
    def __init__(self):
        self.list = []

    def sql(self, acount, pwd):
        self.list = []
        # 打开数据库
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='mysql', charset='utf8')
        # 获取操作游标
        self.cur = self.conn.cursor()
        # 执行SQL语句
        try:
            self.cur.execute("select*from users")
            #     fetchall查询全部结果   fetchone查询单条数据
            self.result = self.cur.fetchall()
            for row in self.result:
                self.uid = row[0]
                self.name = row[1]
                self.pwd = row[2]
                # print("执行结果:" + '\n' + "ID:{}, name:{}, pwd:{}".format(self.uid, self.name, self.pwd))
                if pwd == self.pwd and acount == self.uid:
                    self.list.append(self.name)
                    return True, self.name
                    # print("执行结果:" + '\n' + "ID:{}, name:{}, pwd:{}".format(self.uid, self.name, self.pwd))
                    break
                else:
                    continue
        finally:
            self.conn.close()
