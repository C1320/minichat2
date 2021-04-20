#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/2/3 19:02
# @Author : 十三
# @Email : 2429120006@qq.com
# @Site : 
# @File : Server.py
# @Software: PyCharm
import socket
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import time

users = {}


class Server(QMainWindow):
    def __init__(self, parent=None):
        self.flag = False  # 标志服务器状态
        self.userlist = []  # 用户列表
        # 初始化继承父类
        super(Server, self).__init__(parent)
        self.ServerGui()
        self.setfont()
        self.zhujian()

    def setfont(self):
        # 字体大小
        self.font1 = QtGui.QFont()
        self.font1.setFamily("黑体")
        self.font1.setPointSize(12)
        self.font2 = QtGui.QFont()
        self.font2.setFamily("宋体")
        self.font2.setPointSize(12)
        self.font3 = QtGui.QFont()
        self.font3.setFamily("黑体")
        self.font3.setPointSize(16)

    def run(self, receiveMsg):
        self.user = receiveMsg.recv(1024).decode('utf-8')  # 接受客户端发送的信息以1k作为单位这里接受到的信息为byte类型
        if self.user not in self.userlist:
            self.userlist.append(self.user)  # 添加用户到列表
        users[self.user] = receiveMsg  # 解码并储存用户的信息
        # print(self.userlist)
        # print(receiveMsg)
        self.textMsg.append('用户：[{}]'.format(self.user) + '请求连接服务器成功' + '\n')

        for user in self.userlist:  # 获取在线用户列表
            users[user].send('is_user'.encode('utf-8'))  # 先发送一个信息，表示用户
            for online in self.userlist:
                users[user].send(online.encode('utf-8'))  # 发送用户列表
            time.sleep(1)  # 延时1s（不加，会出现昵称+no_user）
            users[user].send('no_user'.encode('utf-8'))  # 再发送一个信息，表示用户结束
            # print(user)
        while True:
            try:
                self.receiveData = receiveMsg.recv(1024).decode('utf-8')  # 接收客户端的信息
                self.textMsg.append(self.receiveData + '\n')
                us, msg = self.receiveData.split(':')
                print(msg)
                if msg != 'exit':
                    for u in self.userlist:
                        if u != us:
                            # print(u)
                            users[u].send(self.receiveData.encode('utf-8'))
                        else:
                            continue
                elif msg == 'exit':
                    # 删除用户
                    self.userlist.remove(us)
                    # 删除字典中的用户信息
                    del users[us]
                    # 有用户退出，重新发送用户在线列表给每个在线用户
                    for online_user in self.userlist:  # 获取用户在线列表
                        users[online_user].send('user_exit'.encode('utf-8'))  # 先发送一个信息，表示用户退出
                        # for new_online in self.userlist:  # 获取新的用户在线，并发送给每个在线用户
                        users[online_user].send(us.encode('utf-8'))  # 告诉每个在线用户，谁退出
                        time.sleep(0.5)
                        users[online_user].send('user_exit_ok'.encode('utf-8'))  # 发送完一个用户
                    self.textMsg.append(us + '断开连接' + '\n')

            except Exception as e:
                print(e)
                break

    def starts(self):
        self.getIp = self.IP_lineedit.text()
        self.getPort = self.port_lineedit.text()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.getIp, int(self.getPort)))  # 绑定ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
        # 2:bind()的参数是一个元组的形式
        self.socket.listen(10)  # 设置监听，和设置连接的最大的数量
        self.textMsg.append('服务器已启动' + '\n')
        while True:
            if not self.flag:
                receiveMsg, receiveip_port = self.socket.accept()  # 接受所连接的客户端的信息
                t = threading.Thread(target=self.run, args=(receiveMsg,))
                t.start()
            else:
                break

    def startServer(self):
        self.s = threading.Thread(target=self.starts)
        self.s.start()

    def edit_empty(self):  # 判断地址是否为空
        if len(self.IP_lineedit.text()) > 0 and len(self.port_lineedit.text()) > 0:
            self.start_connect.setEnabled(True)
        else:
            self.start_connect.setEnabled(False)

    def select(self):
        if len(self.IP_lineedit.text()) > 0 and len(self.port_lineedit.text()) > 0:
            self.startServer()

    def zhujian(self):
        self.IP = QLabel('IP', self)
        self.IP.setFont(self.font2)
        self.IP.setGeometry(20, 50, 40, 40)
        self.IP_lineedit = QLineEdit(self)
        self.IP_lineedit.setFont(self.font2)
        self.IP_lineedit.setPlaceholderText('请输入IP地址')
        self.IP_lineedit.setGeometry(80, 50, 200, 40)
        # 获取本机IP（socket.gethostname()获取本机名，socket.gethostbyname获取IP）
        self.IP_lineedit.setText(socket.gethostbyname(socket.gethostname()))
        # self.IP_lineedit.setInputMask('000.000.000.000;0')  # ip地址掩码,0为空白符
        self.IP_lineedit.textChanged.connect(self.edit_empty)
        self.port = QLabel('端口', self)
        self.port.setFont(self.font2)
        self.port.setGeometry(20, 120, 40, 40)
        self.port_lineedit = QLineEdit(self)
        self.port_lineedit.setFont(self.font2)
        # 文本水平方向居中显示
        self.port_lineedit.setAlignment(Qt.AlignCenter)
        self.port_lineedit.setText('8080')
        self.IP_lineedit.setAlignment(Qt.AlignCenter)
        self.port_lineedit.setPlaceholderText('请输入端口号')
        self.port_lineedit.setGeometry(80, 120, 200, 40)
        self.port_lineedit.textChanged.connect(self.edit_empty)
        self.connection = '开始连接'
        self.start_connect = QPushButton(self)
        self.start_connect.setFont(self.font2)
        self.start_connect.setText(self.connection)
        # self.start_connect.setEnabled(False)  # 地址为空，不可用状态
        self.start_connect.setGeometry(80, 220, 200, 40)
        self.textMsg = QTextEdit(self)
        self.textMsg.setGeometry(290, 50, 205, 210)
        self.textMsg.setAlignment(Qt.AlignCenter)
        self.textMsg.setReadOnly(True)
        self.start_connect.clicked.connect(self.startServer)
        self.IP_lineedit.returnPressed.connect(self.select)  # 绑定键盘回车键
        self.port_lineedit.returnPressed.connect(self.select)  # 绑定键盘回车键

    def ServerGui(self):
        self.resize(500, 300)
        # 窗口标题
        self.setFixedSize(self.width(), self.height())  # 窗口不可改变
        self.setWindowTitle("服务器")
        # 设置窗口图标
        self.setWindowIcon(QIcon('./imag/Title.ico'))
        # 设置对象名称（不用这个不显示？）
        # self.setObjectName('MainWindow')
        # self.bg = './server.jpg'  # 壁纸
        # self.setStyleSheet("#MainWindow{border-image:url(" + '{}'.format(self.bg) + ");}")
        # # self.setWindowOpacity(0.9)   # 设置窗口透明度

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '客户端',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.flag = True
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    # # 每一个pyqt程序中都需要有一个QApplication对象，sys.argv是一个命令行参数列表
    app = QApplication(sys.argv)
    # # 实例化窗口
    server = Server()
    # # 窗口显示
    server.show()
    # # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())
