# -*- coding: utf-8 -*-
import traceback

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import mysql.connector

from baseFun import connect_database


class Ui_settings(object):
    def setupUi(self, settings):
        settings.setObjectName("settings")
        settings.resize(809, 614)
        self.verticalLayout = QtWidgets.QVBoxLayout(settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.address = QtWidgets.QLabel(self.groupBox)
        self.address.setObjectName("address")
        self.horizontalLayout.addWidget(self.address)
        self.addressinput = QtWidgets.QLineEdit(self.groupBox)
        self.addressinput.setObjectName("addressinput")
        self.horizontalLayout.addWidget(self.addressinput)
        self.port = QtWidgets.QLabel(self.groupBox)
        self.port.setObjectName("port")
        self.horizontalLayout.addWidget(self.port)
        self.portinput = QtWidgets.QLineEdit(self.groupBox)
        self.portinput.setMaximumSize(QtCore.QSize(40, 16777215))
        self.portinput.setObjectName("portinput")
        self.horizontalLayout.addWidget(self.portinput)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.user = QtWidgets.QLabel(self.groupBox)
        self.user.setObjectName("user")
        self.horizontalLayout_2.addWidget(self.user)
        self.userinput = QtWidgets.QLineEdit(self.groupBox)
        self.userinput.setObjectName("userinput")
        self.horizontalLayout_2.addWidget(self.userinput)
        self.password = QtWidgets.QLabel(self.groupBox)
        self.password.setObjectName("password")
        self.horizontalLayout_2.addWidget(self.password)
        self.passwordinput = QtWidgets.QLineEdit(self.groupBox)
        self.passwordinput.setObjectName("passwordinput")
        self.horizontalLayout_2.addWidget(self.passwordinput)
        self.testsqlbutton = QtWidgets.QPushButton(self.groupBox)
        self.testsqlbutton.setObjectName("testsqlbutton")
        self.horizontalLayout_2.addWidget(self.testsqlbutton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.testsqlbutton.clicked.connect(self.connect_database)

        self.retranslateUi(settings)
        QtCore.QMetaObject.connectSlotsByName(settings)

    def retranslateUi(self, settings):
        _translate = QtCore.QCoreApplication.translate
        settings.setWindowTitle(_translate("settings", "设置"))
        self.groupBox.setTitle(_translate("settings", "数据库设置"))
        self.address.setText(_translate("settings", "地址"))
        self.port.setText(_translate("settings", "端口"))
        self.user.setText(_translate("settings", "用户名"))
        self.password.setText(_translate("settings", "密码"))
        self.testsqlbutton.setText(_translate("settings", "测试"))

    def connect_database(self):
        address = self.addressinput.text()
        port = self.portinput.text()
        user = self.userinput.text()
        password = self.passwordinput.text()
        try:
            mydb = mysql.connector.connect(
            host=str(address),
            port=int(port),
            user=str(user),
            passwd=str(password))
            cursor = mydb.cursor()
            print('成功')
        except Exception as e:
            print('失败')
            traceback.print_exc()

class Setting(QWidget,Ui_settings):
    def __init__(self):
        super(Setting, self).__init__()
        self.setupUi(self)