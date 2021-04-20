#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/1/20 15:29
# @Author : 十三
# @Email : 2429120006@qq.com
# @Site : 
# @File : MainPanel2.py
# @Software: PyCharm
import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import socket, threading
import time


class MainWind_2(QMainWindow):
    def __init__(self, name, parent=None):
        super(MainWind_2, self).__init__(parent)
        self.Online_list = []  # 在线用户
        self.flag = False  # 标志与服务器连接状态，默认没有连接
        self.close_flag = False  # 标志窗口是否关闭，默认不关闭
        self.user_flag = 0  # 用户标志,默认表示接受信息
        self.title = name  # 标题
        self.Name = name
        self.users = {}  # 用户字典，也可以连接数据库
        self.Initfont()
        self.client()

    def sendText(self):

        self.senData = self.send_text.toPlainText()  # 获取发送内容
        if len(self.senData) > 0:  # 发送内容不空
            self.client_socket.send((self.username_lineedit.text() + ':' + self.senData).encode('utf-8'))
            # 获取时间
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
            self.chat_text.setFont(self.font2)
            self.chat_text.setAlignment(Qt.AlignRight)
            self.chat_text.setTextColor(QColor('BlueViolet'))
            self.chat_text.insertPlainText('[{}]'.format(self.username_lineedit.text()) + now_time)
            self.chat_text.setTextColor(QColor('Blue'))
            self.chat_text.insertPlainText(self.senData + '\n')
        else:
            QMessageBox.information(self, '提示', '内容不能为空',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def Button_state(self):  # 按钮状态
        if self.start_connect.text() == '开始连接':
            self.server()
        elif self.start_connect.text() == '断开连接':
            self.disconnect()

    def disconnect(self):  # 断开连接
        # 断开连接，发送信息给服务器
        self.client_socket.send((self.username_lineedit.text() + ':' + 'exit').encode('utf-8'))
        self.flag_label.setText('状态：未连接')
        self.IP_lineedit.setEnabled(True)
        self.port_lineedit.setEnabled(True)
        self.username_lineedit.setEnabled(True)
        self.start_connect.setText('开始连接')
        self.start_connect.setEnabled(False)
        self.IP_lineedit.clear()  # 清空
        self.port_lineedit.clear()
        self.username_lineedit.clear()
        print("连接已断开")

    def getDta(self):
        while True:
            try:
                if not self.close_flag:
                    self.Data = self.client_socket.recv(1024).decode('utf-8')
                    print(self.Data)
                    if self.Data == 'is_user':
                        while True:
                            Data = self.client_socket.recv(1024).decode('utf-8')
                            if Data != 'no_user' and Data not in self.Online_list:  # 开始用户不在列表进行添加
                                self.Online_list.append(Data)
                                self.Online_count.setText(str(len(self.Online_list)))
                                self.Online.addItem(Data)
                            elif Data == 'no_user':
                                break
                    elif self.Data == 'user_exit':
                        while True:
                            del_user = self.client_socket.recv(1024).decode('utf-8')
                            if del_user != 'user_exit_ok' and del_user in self.Online_list:
                                self.Online_list.remove(del_user)
                                self.Online_count.setText(str(len(self.Online_list)))
                                self.Online.clear()
                                time.sleep(0.5)
                                for user in self.Online_list:
                                    self.Online.addItem(user)
                            elif self.Data == 'user_exit_ok':
                                # 告诉服务器信息收到成功
                                self.client_socket.send('recv:exit_ok'.encode('utf-8'))
                                break
                    else:
                        # self.user_flag = True
                        self.chat_text.setAlignment(Qt.AlignLeft)  # 对接收到的信息显示在左边
                        self.chat_text.setFont(self.font2)
                        # 获取时间
                        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
                        self.chat_text.setTextColor(QColor('BlueViolet'))
                        self.chat_text.insertPlainText(('[{}]'.format(self.Data.split(":")[0]) + now_time))
                        self.chat_text.setTextColor(QColor('DarkRed'))
                        self.chat_text.insertPlainText(self.Data.split(':')[1] + '\n')
                else:
                    break
            except Exception as e:
                print(e)

    def server(self):
        self.flag = True
        self.IP_lineedit.setEnabled(False)  # 连接成功，不可编辑
        self.port_lineedit.setEnabled(False)
        self.username_lineedit.setEnabled(False)
        self.start_connect.setText('断开连接')
        self.flag_label.setText('状态：已连接')
        self.getip = self.IP_lineedit.text()  # 获取IP
        self.getport = self.port_lineedit.text()  # 获取端口
        self.name = self.username_lineedit.text()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.getip, int(self.getport)))
        self.client_socket.send(self.name.encode('utf-8'))
        self.thead()

    def thead(self):
        self.send.clicked.connect(self.sendText)
        t = threading.Thread(target=self.getDta)
        t.start()

    def edit_empty(self):  # 判断地址是否为空
        if len(self.IP_lineedit.text()) > 0 and len(self.port_lineedit.text()) > 0 and len(
                self.username_lineedit.text()) > 0:
            self.start_connect.setEnabled(True)
        else:
            self.start_connect.setEnabled(False)

    def Initfont(self):  # 字体
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

    # 字体选择
    def getFont(self):
        font, ok = QFontDialog.getFont(self)
        if ok:
            self.send_text.setFont(font)

    def openFile(self):  # 打开文件
        self.dig = QFileDialog(self)  # 实例化QFileDialog
        self.dig.setFileMode(QFileDialog.AnyFile)  # 设置可以打开任何文件
        self.dig.setFilter(QDir.Files)  # 文件过滤
        if self.dig.exec_():
            self.filenames = self.dig.selectedFiles()  # 接受选中文件的路径，默认为列表
            self.send_text.insertPlainText(self.filenames[0])   # 第一个即为文件路径

    def client(self):  # 登录成功
        self.resize(1000, 600)
        # 窗口标题
        self.setFixedSize(self.width(), self.height())  # 窗口不可改变
        self.setWindowIcon(QIcon('../imag/Title.ico'))  # 设置窗口图标
        self.setWindowTitle(self.title)
        '''
        创建一个Frame,左区域
        '''
        self.left = QFrame(self)
        self.left.resize(300, 600)
        self.left.setFrameShape(QFrame.Box)  # 设置图形为：Box
        self.left.setFrameRect(QRect(0, 0, 300, 600))  # 这是边框
        self.left.setStyleSheet("background-color:LightBLue;")  # 背景颜色
        '''
        右上区域
        '''
        self.right_top = QFrame(self)
        self.right_top.resize(700, 500)
        self.right_top.setFrameShape(QFrame.Box)  # 设置图形为：Box
        self.right_top.setFrameRect(QRect(300, 0, 900, 500))  # 这是边框
        # self.left.setStyleSheet("background-color:LightCyan;")   # 背景颜色
        self.IP = QLabel('IP', self)
        self.IP.setFont(self.font2)
        self.IP.setGeometry(20, 50, 40, 40)
        self.IP_lineedit = QLineEdit(self)
        # 文本水平方向居中显示
        self.IP_lineedit.setAlignment(Qt.AlignCenter)
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
        self.port_lineedit.setPlaceholderText('请输入端口号')
        self.port_lineedit.setGeometry(80, 120, 200, 40)
        self.port_lineedit.textChanged.connect(self.edit_empty)

        self.username = QLabel('昵称', self)
        self.username.setFont(self.font2)
        self.username.setGeometry(20, 190, 40, 40)
        self.username_lineedit = QLineEdit(self)
        self.username_lineedit.setFont(self.font2)
        # 文本水平方向居中显示
        self.username_lineedit.setAlignment(Qt.AlignCenter)
        self.username_lineedit.setText(self.Name)
        self.username_lineedit.setPlaceholderText('请输入昵称')
        self.username_lineedit.setGeometry(80, 190, 200, 40)
        self.username_lineedit.textChanged.connect(self.edit_empty)
        # self.senwho_lineedit = QLineEdit(self)
        # self.senwho_lineedit.setFont(self.font2)
        # self.senwho_lineedit.setPlaceholderText('对方昵称')
        # self.senwho_lineedit.setGeometry(80, 330, 200, 40)

        '''
        连接按钮
        '''
        self.connection = '开始连接'
        self.start_connect = QPushButton(self)
        self.start_connect.setFont(self.font2)
        self.start_connect.setText(self.connection)
        # self.start_connect.setEnabled(False)  # 地址为空，不可用状态
        self.start_connect.setGeometry(80, 250, 200, 40)
        self.start_connect.clicked.connect(self.Button_state)
        '''
        连接状态
        '''
        self.connection_flag = '状态：未连接'
        self.flag_label = QLabel(self)
        self.flag_label.setText(self.connection_flag)
        self.flag_label.setGeometry(130, 290, 100, 40)
        ''''
        用户在线
        '''
        self.Online_label = QLabel(self)
        self.Online_label.setText('当前在线：')
        self.Online_label.setGeometry(80, 350, 100, 40)
        self.Online_label.setFont(self.font2)
        self.Online_count = QLabel(self)
        self.Online_count.setText('0')
        self.Online_count.setGeometry(180, 350, 60, 40)
        self.Online_count.setFont(self.font2)
        self.Online = QListWidget(self)
        # self.Online.setReadOnly(True)  # 只读
        self.Online.setGeometry(80, 380, 200, 218)
        self.Online.setStyleSheet("background-color:LightBLue;")  # 背景颜色
        '''
        会话窗口
        '''
        self.str = ' '
        self.chat_label = QLabel(self)
        self.chat_label.setFont(self.font1)
        self.chat_label.setText(self.str * 30 + '会话窗口')
        self.chat_label.setGeometry(300, 0, 700, 40)
        self.chat_label.setStyleSheet("background-color:LightCyan;")
        '''
        文本显示内容
        '''
        self.chat_text = QTextEdit(self)
        self.chat_text.setReadOnly(True)  # 只读状态
        self.chat_text.setGeometry(300, 40, 700, 460)
        '''
        字体等控件
        '''
        self.select_font = QPushButton(self)  # 发送按钮
        self.select_font.setText('')
        self.select_font.setStyleSheet('''
                                                      border-image: url(../imag/font.jpg);
                                                      ''')
        # self.select_font.setIcon(QIcon('../imag/font.jpg'))  # 设置图标
        self.select_font.setIconSize(QSize(50, 50))  # 图标大小
        self.select_font.setGeometry(300, 500, 40, 40)
        self.select_font.clicked.connect(self.getFont)
        '''
        文件
        '''
        self.file = QPushButton(self)  # 发送按钮
        self.file.setText('')
        self.file.setStyleSheet('''
                                              border-image: url(../imag/file.jpg);
                                              ''')
        # self.file.setIcon(QIcon('../imag/file.jpg'))  # 设置图标
        self.file.setIconSize(QSize(50, 50))  # 图标大小
        self.file.setGeometry(350, 500, 50, 50)
        self.file.clicked.connect(self.openFile)
        '''
        图片
        '''
        self.photo = QPushButton(self)  # 发送按钮
        self.photo.setText('')
        self.photo.setStyleSheet('''
                                      border-image: url(../imag/photo.jpg);
                                      ''')
        # self.photo.setIcon(QIcon('../imag/photo.jpg'))  # 设置图标
        self.photo.setIconSize(QSize(50, 50))  # 图标大小
        self.photo.setGeometry(420, 500, 50, 50)
        '''
        相机
        '''
        self.camera = QPushButton(self)  # 发送按钮
        self.camera.setText('')
        self.camera.setStyleSheet('''
                               border-image: url(../imag/camera.jpg);
                               ''')
        # self.camera.setIcon(QIcon('../imag/camera.jpg'))  # 设置图标
        self.camera.setIconSize(QSize(50, 50))  # 图标大小
        self.camera.setGeometry(490, 500, 50, 50)
        '''
        视频
        '''
        self.video = QPushButton(self)  # 发送按钮
        self.video.setText('')
        self.video.setStyleSheet('''
                       border-image: url(../imag/video.jpg);
                       ''')
        # self.video.setIcon(QIcon('../imag/video.jpg'))  # 设置图标
        self.video.setIconSize(QSize(50, 50))  # 图标大小
        self.video.setGeometry(560, 500, 50, 50)
        '''
        表情包
        '''
        self.expression = QPushButton(self)  # 发送按钮
        self.expression.setText('')
        self.expression.setStyleSheet('''
                border-image: url(../imag/expression.jpg);
                ''')
        # self.expression.setIcon(QIcon('../imag/expression.jpg'))  # 设置图标
        self.expression.setIconSize(QSize(50, 50))  # 图标大小
        self.expression.setGeometry(630, 500, 50, 50)
        '''
        发送内容
        '''
        self.send_text = QTextEdit(self)
        self.send_text.setFont(self.font1)
        self.send_text.setPlaceholderText('请输入发送内容')
        self.send_text.setGeometry(300, 545, 600, 50)
        '''
        按钮
        '''
        self.send = QPushButton(self)  # 发送按钮
        self.send.setFont(self.font2)
        self.send.setText('发送')
        self.send.setIcon(QIcon('../imag/send.jpg'))  # 登录图标
        self.send.setGeometry(905, 545, 95, 50)

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
            if not self.flag:
                event.accept()
            else:
                self.client_socket.send((self.username_lineedit.text() + ':' + 'exit').encode('utf-8'))
                # 退出程序，清除登录信息
                # with open('./file/info.txt', 'w+', encoding='utf-8') as fp:
                #     fp.write(','.join(('', '', '')))
                self.close_flag = True
                event.accept()
        else:
            event.ignore()
