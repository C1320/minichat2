#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/1/20 15:29
# @Author : 十三
# @Email : 2429120006@qq.com
# @Site : 
# @File : login2.py
# @Software: PyCharm
import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Client2.MainPanel2 import MainWind_2
from cyq_sql import L_sql
from remenber_sql import reb_sql


class Login_2(QMainWindow):
    def __init__(self, parent=None):
        # 初始化继承父类
        super(Login_2, self).__init__(parent)
        try:
            with open('./file/info.txt', 'r+', encoding='utf-8') as fp:
                self.c, self.p, N = fp.read().strip().split(',')

        except:
            pass
        # 初始化界面
        self.GUI()
        # 编辑函数
        self.Edit()
        # 状态栏显示,时间5s
        self.status.showMessage("欢迎使用", 5000)
        self.list = reb_sql().find_sql()  # 实例化reb_sql，返回得到存储账号列表，用于自动补全
        self.init_complete()

    def init_complete(self):  # 初始化补全器
        self.completer = QCompleter(self.list)  # 增加自动补全
        '''
        # 设置匹配模式  有三种： 
        Qt.MatchStartsWith 开头匹配（默认）  
        Qt.MatchContains 内容匹配  
        Qt.MatchEndsWith 结尾匹配
        '''
        self.completer.setFilterMode(Qt.MatchContains)  # 内容匹配
        '''
         # 设置补全模式  有三种： 
         QCompleter.PopupCompletion（默认）  
         QCompleter.InlineCompletion   
         QCompleter.UnfilteredPopupCompletion
        '''
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.Account.setCompleter(self.completer)  # 给Account设置补全器

    def main(self):
        # L_sql().sql(self.Account.text(),self.passwd.text())
        self.sq = L_sql()  # 实例化l_sql类
        if len(self.Account.text()) > 0 and len(self.passwd.text()) > 0:  # 判断账号密码不为空
            self.bo, self.name = self.sq.sql(self.Account.text(), self.passwd.text())  # 接收数据库中返回信息
            if self.bo:
                # 判断账号是否已登录
                # if self.c != self.Account.text():
                reb_sql().insert_sql(self.Account.text(), self.name)  # 实例化reb_sql，并调用insert_sql函数
                # #     登录成功，把相关账户昵称信息写入临时文件
                # with open('./file/info.txt', 'w+', encoding='utf-8') as fp:
                #     fp.write(','.join((self.Account.text(), self.passwd.text(), self.name)))
                '''
                注意：登录成功后，展示新窗口必须用self.(),否则新窗体会闪退
                '''
                self.main_gui = MainWind_2(self.name)  # 生成主窗口的实例
                self.main_gui.show()  # 显示主窗口
                self.close()  # 关闭登录窗口
                # else:
                self.status.showMessage('该账号已登录', 5000)
                self.status.setFont(self.font1)  # 字体大小
                self.status.setStyleSheet("color:Khaki")  # 字体颜色
            else:
                self.status.showMessage('登录失败', 5000)
                self.status.setFont(self.font1)  # 字体大小
                self.status.setStyleSheet("color:Khaki")  # 字体颜色
        else:
            QMessageBox.information(self, '提示', '账号或密码不能为空',
                                    QMessageBox.Retry | QMessageBox.Retry, QMessageBox.Yes)

    # 判断是否可登录状态
    def enable(self):
        if len(self.Account.text()) <= 0:
            self.login_bt.setEnabled(False)
            # self.pwd.setEnabled(False)  # 账号无输入时，密码框不可编辑
        else:
            self.login_bt.setEnabled(True)
            # self.pwd.setEnabled(True)    # 账号输入时，密码框可编辑

    def wallpaper(self, q):  # 壁纸
        if q.text() == '更换壁纸':
            self.dig = QFileDialog()  # 实例化QFileDialog
            self.dig.setFileMode(QFileDialog.AnyFile)  # 设置可以打开任何文件
            self.dig.setFilter(QDir.Files)  # 文件过滤
            if self.dig.exec_():
                self.filenames = self.dig.selectedFiles()  # 接受选中文件的路径，默认为列表
                self.bg = self.filenames[0]  # 列表中的第一个元素即是文件路径，以只读的方式打开文件
                self.setStyleSheet("#MainWindow{border-image:url(" + '{}'.format(self.bg) + ");}")
                print(self.bg)

    def Edit(self):
        # 设置透明度
        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0.8)
        """
        头像
        :return:
        """
        self.Avatar = QLabel(self)
        self.Avatar.setGeometry(QtCore.QRect(200, 70, 130, 130))
        self.Avatar.setGraphicsEffect(self.op)
        self.Avatar.setStyleSheet('''
                                                     border-image: url(../imag/head.gif);
                                                     ''')
        # 账号Label
        self.Account_Label = QLabel(self)
        # 设置Label文本内容
        self.Account_Label.setText('账号：')
        # 账号Label位置
        self.Account_Label.setGeometry(QtCore.QRect(120, 230, 70, 40))
        self.Account_Label.setPixmap(QPixmap('../imag/user1.png'))
        # 字体大小
        self.font1 = QtGui.QFont()
        self.font1.setFamily("楷体")
        self.font1.setPointSize(16)
        self.Account_Label.setFont(self.font1)
        # self.Account_Label.move(100, 80)
        # 密码同上
        self.passwd_Label = QLabel(self)
        self.passwd_Label.setText('密码：')
        self.passwd_Label.setGeometry(QtCore.QRect(120, 300, 70, 40))
        self.passwd_Label.setFont(self.font1)
        self.passwd_Label.setPixmap(QPixmap('../imag/pwd.png'))
        # self.passwd_Label.move(100, 150)
        # 账号密码单行文本输入框
        # 字体大小
        self.font2 = QtGui.QFont()
        self.font2.setFamily("黑体")
        self.font2.setPointSize(16)

        self.Account = QLineEdit(self)
        self.Account.setWindowIcon(QIcon("../imag/user.jpg"))
        # 输入框位置、大小
        self.Account.setGeometry(QtCore.QRect(158, 230, 250, 40))
        # 设置提示文本
        self.Account.setPlaceholderText('请输入账号')
        # 文本水平方向居中显示
        self.Account.setAlignment(Qt.AlignCenter)
        self.Account.setFont(self.font2)
        # 设置文本最大长度
        self.Account.setMaxLength(16)
        # 设置清除内容按钮
        self.Account.setClearButtonEnabled(True)
        self.Account.setGraphicsEffect(self.op)
        self.Account.textChanged.connect(self.enable)
        self.Account.returnPressed.connect(self.main)  # 绑定键盘回车键
        # self.Account.move(180, 80)
        self.passwd = QLineEdit(self)
        # self.pwd.setEnabled(False)            # 开始密码框处于不可编辑状态
        self.passwd.setClearButtonEnabled(True)
        self.passwd.setAlignment(Qt.AlignCenter)
        self.passwd.setMaxLength(16)
        self.passwd.setPlaceholderText('请输入密码')
        # 设置回显方式
        self.passwd.setEchoMode(QLineEdit.Password)
        # 输入框位置、大小
        self.passwd.setGeometry(QtCore.QRect(158, 300, 250, 40))
        self.passwd.setFont(self.font2)
        self.passwd.returnPressed.connect(self.main)  # 绑定键盘回车键
        # self.pwd.move(180, 150)
        '''
        添加控件
        '''
        self.login_bt = QPushButton(self)
        self.login_bt.setShortcut(Qt.Key_Enter)
        # self.login_bt.setDefault(True)  # 默认按钮
        # 开始按钮处于不可用状态
        # self.login_bt.setEnabled(False)
        self.login_bt.setFont(self.font1)
        self.login_bt.setText('立即登录')
        self.login_bt.setGeometry(QtCore.QRect(180, 400, 200, 60))
        self.login_bt.setGraphicsEffect(self.op)
        self.login_bt.setIcon(QIcon('../imag/commit.jpg'))  # 登录图标
        # 信号绑定
        self.login_bt.clicked.connect(self.main)

        '''
        菜单栏
        '''
        self.mbar = self.menuBar()
        self.SET = self.mbar.addMenu('设置')  # 向菜单栏中添加新的QMenu对象，父菜单
        self.SET.setFont(self.font1)
        self.SET.setIcon(QIcon('../imag/set.jpg'))
        self.SET.addAction('字体')
        self.SET.addAction('更换壁纸')
        self.SET.triggered[QAction].connect(self.wallpaper)  # 单击任何Qmenu对象，都会发射信号，绑定槽函数
        self.operating = self.mbar.addMenu('操作')
        self.operating.setFont(self.font1)
        self.operating.setIcon(QIcon('../imag/about.jpg'))
        self.operating.addAction('注册用户')
        self.operating.addAction('修改密码')
        self.operating.addAction('找回密码')
        self.about = self.mbar.addMenu('关于')
        self.about.setFont(self.font1)
        self.about.setIcon(QIcon('../imag/operating.jpg'))
        self.about.addAction('作者   十三')
        self.about.addAction('版本 V1.0.0')
        self.help = self.mbar.addMenu('帮助')
        self.help.setFont(self.font1)
        self.help.setIcon(QIcon('../imag/help.jpg'))
        self.help.addAction('使用指南')
    def GUI(self):
        # 窗口大小
        self.resize(500, 500)
        # 实例化状态栏
        self.status = self.statusBar()
        # 窗口标题
        self.setFixedSize(self.width(), self.height())  # 窗口不可改变
        self.setWindowTitle("闲聊2")
        # 设置窗口图标
        self.setWindowIcon(QIcon('../imag/Title.ico'))
        # 设置对象名称（不用这个不显示？）
        self.setObjectName('MainWindow')
        self.bg = '../imag/bg.jpg'  # 壁纸
        self.setStyleSheet("#MainWindow{border-image:url(" + '{}'.format(self.bg) + ");}")
        # self.setWindowOpacity(0.9)   # 设置窗口透明度


if __name__ == '__main__':
    # # 每一个pyqt程序中都需要有一个QApplication对象，sys.argv是一个命令行参数列表
    app = QApplication(sys.argv)
    # # 实例化窗口
    form = Login_2()
    # main_gui = MainWind_2()  # 生成主窗口的实例
    # # 窗口显示
    form.show()
    # # 进入程序的主循环，遇到退出情况，终止程序
    sys.exit(app.exec_())
