# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stockinfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class Ui_stockinfo(object):
    def setupUi(self, stockinfo):
        stockinfo.setObjectName("stockinfo")
        stockinfo.resize(300, 123)
        stockinfo.setMaximumSize(QtCore.QSize(300, 123))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(stockinfo)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(stockinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(stockinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(stockinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.trade_date = QtWidgets.QComboBox(stockinfo)
        self.trade_date.setObjectName("trade_date")
        self.verticalLayout_2.addWidget(self.trade_date)
        self.price = QtWidgets.QLineEdit(stockinfo)
        self.price.setObjectName("price")
        self.verticalLayout_2.addWidget(self.price)
        self.num = QtWidgets.QLineEdit(stockinfo)
        self.num.setObjectName("num")
        self.verticalLayout_2.addWidget(self.num)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.pushButton = QtWidgets.QPushButton(stockinfo)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)

        self.retranslateUi(stockinfo)
        QtCore.QMetaObject.connectSlotsByName(stockinfo)

    def retranslateUi(self, stockinfo):
        _translate = QtCore.QCoreApplication.translate
        stockinfo.setWindowTitle(_translate("stockinfo", "股票信息"))
        self.label_3.setText(_translate("stockinfo", "购买日期"))
        self.label_2.setText(_translate("stockinfo", "购买价格"))
        self.label.setText(_translate("stockinfo", "购买数量"))
        self.pushButton.setText(_translate("stockinfo", "确认"))



class StockInfoUI(QWidget, Ui_stockinfo):
    def __init__(self):
        super(StockInfoUI, self).__init__()
        self.setupUi(self)
        self.refresh()
        # self.set_unedit(0)