# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from back import Backall_resize
from Holder import HolderUI
from customer import Customer
from setting import Setting

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1250, 678)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.holder = HolderUI()
        self.backtest = Backall_resize()
        self.customer = Customer()
        self.setting = Setting()
        self.tabWidget.addTab(self.holder,"持股列表")
        self.tabWidget.addTab(self.backtest,"批量回测")
        self.tabWidget.addTab(self.customer, "自定义回测")
        self.tabWidget.addTab(self.setting, "设置")
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged['int'].connect(self.holder.refresh)
        self.tabWidget.currentChanged['int'].connect(self.backtest.refresh_list)
        self.tabWidget.currentChanged['int'].connect(self.customer.refresh_list)
        self.holder.realtestbutton.clicked.connect(self.turn)
        # self.tabWidget.currentChanged[3].connect(self.holder.refresh)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "策略二"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.holder), _translate("MainWindow", "持股列表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.backtest), _translate("MainWindow", "批量回测"))


    def turn(self):
        self.tabWidget.setCurrentIndex(2)


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.setupUi(self)
