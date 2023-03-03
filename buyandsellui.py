# -*- coding: utf-8 -*-
import os
import sys

# Form implementation generated from reading ui file 'buyandsellui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QHeaderView, QAbstractItemView
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class Ui_buyandsell(object):
    def setupUi(self, buyandsell):
        buyandsell.setObjectName("buyandsell")
        buyandsell.resize(1400, 850)
        buyandsell.setMinimumSize(QtCore.QSize(1400, 850))
        buyandsell.setMaximumSize(QtCore.QSize(1400, 850))
        self.centralwidget = QtWidgets.QWidget(buyandsell)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(190, 20, 411, 241))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['日期', '买卖', '价格'])
        # self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        # self.textEdit.setGeometry(QtCore.QRect(33, 290, 751, 421))
        # self.textEdit.setObjectName("textEdit")
        buyandsell.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(buyandsell)
        self.statusbar.setObjectName("statusbar")
        buyandsell.setStatusBar(self.statusbar)
        # self.textEdit.setReadOnly(True)

        self.retranslateUi(buyandsell)
        QtCore.QMetaObject.connectSlotsByName(buyandsell)

    def retranslateUi(self, buyandsell):
        _translate = QtCore.QCoreApplication.translate
        buyandsell.setWindowTitle(_translate("buyandsell", "买卖详情"))

    def get_html(self):
        html = ""
        with open("min_kline.html", "r", encoding="utf-8") as f:
            html = f.read()
        return html


class BuyandSell(QMainWindow, Ui_buyandsell):
    def __init__(self):
        super(BuyandSell, self).__init__()
        self.setupUi(self)
        self.browser = QWebEngineView()
        # url = os.getcwd() + os.path.sep + 'min_kline.html'
        # url = os.getcwd() + os.path.sep + 'windataFalse'+'\\'+'300933SZ.html'
        # print(url)
        # self.browser.load(QUrl.fromLocalFile(url))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        lay = QGridLayout(self.central_widget)
        lay.addWidget(self.browser, 1, 0,1,2)
        lay.addWidget(self.tableWidget, 0, 0,1,2)
        lay.setColumnStretch(0, 1)
        lay.setColumnStretch(1, 2)
        lay.setRowStretch(0, 1)
        lay.setRowStretch(1, 3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = BuyandSell()
    test.show()
    sys.exit(app.exec_())
