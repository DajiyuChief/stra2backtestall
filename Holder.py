# -*- coding: utf-8 -*-
import multiprocessing
import os
import threading
import time
import traceback

import pandas as pd
# Form implementation generated from reading ui file 'Holder.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QItemDelegate

from MessageBox import MessageBox
from gol_all import set_value, get_value
from baseFun import get_name, get_stock_code, hold_stock, create_holdstock_csv, write_to_csv, split_list_n_list, \
    check_process_running
from load_csvdata import load_winning_code
from stockinfo import StockInfoUI
from trade_strategy2 import run


class Ui_Holder(object):
    def setupUi(self, Holder):
        Holder.setObjectName("Holder")
        Holder.resize(1245, 600)
        Holder.setMinimumSize(QtCore.QSize(920, 600))
        Holder.setMaximumSize(QtCore.QSize(999999, 9999999))
        self.centralwidget = QtWidgets.QWidget(Holder)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.holderlist = QtWidgets.QTableWidget(self.groupBox_2)
        self.holderlist.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.holderlist.setObjectName("holderlist")
        self.holderlist.setColumnCount(9)
        self.holderlist.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.holderlist.setHorizontalHeaderItem(8, item)
        self.holderlist.horizontalHeader().setStretchLastSection(False)
        self.holderlist.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_2.addWidget(self.holderlist)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(100, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(150, 400))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")

        self.rsi = QtWidgets.QLineEdit(self.groupBox)
        self.rsi.setMaximumSize(QtCore.QSize(16777215, 35))
        self.rsi.setObjectName("rsi")
        self.verticalLayout.addWidget(self.rsi)

        self.stoploss = QtWidgets.QLineEdit(self.groupBox)
        self.stoploss.setMaximumSize(QtCore.QSize(16777215, 35))
        self.stoploss.setObjectName("stoploss")
        self.verticalLayout.addWidget(self.stoploss)

        self.codeinput = QtWidgets.QLineEdit(self.groupBox)
        self.codeinput.setMaximumSize(QtCore.QSize(16777215, 35))
        self.codeinput.setObjectName("codeinput")
        self.verticalLayout.addWidget(self.codeinput)

        self.downnotbuy = QtWidgets.QCheckBox(self.groupBox)
        self.downnotbuy.setChecked(True)
        self.downnotbuy.setObjectName("downnotbuy")
        self.verticalLayout.addWidget(self.downnotbuy)

        self.addbutton = QtWidgets.QPushButton(self.groupBox)
        self.addbutton.setObjectName("addbutton")
        self.verticalLayout.addWidget(self.addbutton)

        self.deletebutton = QtWidgets.QPushButton(self.groupBox)
        self.deletebutton.setObjectName("deletebutton")
        self.verticalLayout.addWidget(self.deletebutton)

        self.savebutton = QtWidgets.QPushButton(self.groupBox)
        self.savebutton.setObjectName("savebutton")
        self.verticalLayout.addWidget(self.savebutton)

        self.refreshbutton = QtWidgets.QPushButton(self.groupBox)
        self.refreshbutton.setObjectName("refreshbutton")
        self.verticalLayout.addWidget(self.refreshbutton)

        self.buybutton = QtWidgets.QPushButton(self.groupBox)
        self.buybutton.setObjectName("buybutton")
        self.verticalLayout.addWidget(self.buybutton)

        # self.sellbutton = QtWidgets.QPushButton(self.groupBox)
        # self.sellbutton.setObjectName("sellbutton")
        # self.verticalLayout.addWidget(self.sellbutton)

        self.realtestbutton = QtWidgets.QPushButton(self.groupBox)
        self.realtestbutton.setObjectName("realtestbutton")
        self.verticalLayout.addWidget(self.realtestbutton)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        Holder.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Holder)
        self.statusbar.setObjectName("statusbar")
        Holder.setStatusBar(self.statusbar)
        self.holderlist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.retranslateUi(Holder)
        QtCore.QMetaObject.connectSlotsByName(Holder)
        self.holderlist.setAlternatingRowColors(True)
        self.holderlist.horizontalHeader().setSectionsClickable(True)
        self.holderlist.horizontalHeader().setSortIndicatorShown(True)
        self.orderType = Qt.AscendingOrder

        # self.holderlist.setItemDelegateForColumn(0, EmptyDelegate(self))  # 设置第一列不可编辑

        self.holderlist.setItemDelegateForColumn(1, EmptyDelegate(self))  # 设置第二列不可编辑
        self.holderlist.setItemDelegateForColumn(2, EmptyDelegate(self))
        self.holderlist.setItemDelegateForColumn(3, EmptyDelegate(self))
        self.holderlist.setItemDelegateForColumn(4, EmptyDelegate(self))
        self.holderlist.setItemDelegateForColumn(5, EmptyDelegate(self))
        self.holderlist.setItemDelegateForColumn(6, EmptyDelegate(self))  # 设置第7列不可编辑
        self.holderlist.setItemDelegateForColumn(7, EmptyDelegate(self))  # 设置第8列不可编辑
        self.holderlist.setItemDelegateForColumn(8, EmptyDelegate(self))  # 设置第9列不可编辑

        self.refreshbutton.clicked.connect(self.refresh)
        self.refreshbutton.clicked.connect(self.refresh_upper_percent)
        self.addbutton.clicked.connect(self.add_stock)
        self.savebutton.clicked.connect(self.save)
        self.holderlist.cellChanged.connect(self.check)
        # self.holderlist.currentCellChanged.connect(self.cellchange)
        self.deletebutton.clicked.connect(self.delete)
        self.holderlist.horizontalHeader().sectionClicked.connect(self.sort_by_column)
        self.buybutton.clicked.connect(self.buy)
        self.realtestbutton.clicked.connect(self.real_test)
        # self.holderlist.currentCellChanged.connect((self.check))

        self.path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'
        self.message = MessageBox()
        self.stockinfo = StockInfoUI()

        self.rsi.setPlaceholderText('rsi变化率')
        self.rsi.setText('0.1')
        self.stoploss.setPlaceholderText('止损率')
        self.stoploss.setText('0.2')

        self.codeinput.setPlaceholderText('代码或交易股数')

        # 连接信号
        self.stockinfo.param_signal.connect(self.add_code_rest)
    def retranslateUi(self, Holder):
        _translate = QtCore.QCoreApplication.translate
        Holder.setWindowTitle(_translate("Holder", "持股列表"))
        self.groupBox_2.setTitle(_translate("Holder", "持股列表"))
        item = self.holderlist.horizontalHeaderItem(0)
        item.setText(_translate("Holder", "股票代码"))
        item = self.holderlist.horizontalHeaderItem(1)
        item.setText(_translate("Holder", "股票名称"))
        item = self.holderlist.horizontalHeaderItem(2)
        item.setText(_translate("Holder", "首次买入时间"))
        item = self.holderlist.horizontalHeaderItem(3)
        item.setText(_translate("Holder", "首次买入价格"))
        item = self.holderlist.horizontalHeaderItem(4)
        item.setText(_translate("Holder", "当前成本价"))
        item = self.holderlist.horizontalHeaderItem(5)
        item.setText(_translate("Holder", "持股数量"))
        item = self.holderlist.horizontalHeaderItem(6)
        item.setText(_translate("Holder", "当前持股市值"))
        item = self.holderlist.horizontalHeaderItem(7)
        item.setText(_translate("Holder", "收益率"))
        item = self.holderlist.horizontalHeaderItem(8)
        item.setText(_translate("Holder", "同期间股票涨幅"))
        self.groupBox.setTitle(_translate("Holder", "操作"))
        self.realtestbutton.setText(_translate("Holder", "实时检测"))
        self.addbutton.setText(_translate("Holder", "手动添加"))
        self.savebutton.setText(_translate("Holder", "保存"))
        self.refreshbutton.setText(_translate("Holder", "刷新"))
        self.deletebutton.setText(_translate("Holder", "删除"))
        # self.sellbutton.setText(_translate("Holder", "卖出"))
        self.buybutton.setText(_translate("Holder", "交易"))
        self.downnotbuy.setText(_translate("customer", "MA下行不买入"))

    def refresh(self):
        try:
            self.holderlist.blockSignals(True)
            # 设置全局变量 方便增删改查
            path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'
            df = pd.read_csv(path)
            set_value('df_holdlist', df)
            # df = pd.DataFrame(get_value('df_holdlist'))
            if df.empty:
                return
            values_list = df.values.tolist()
            self.holderlist.setRowCount(len(values_list))
            for row in range(len(values_list)):
                code_text = QTableWidgetItem(QTableWidgetItem(values_list[row][0]))
                code = QtWidgets.QTableWidgetItem(code_text)
                code.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                first_buy_date = QTableWidgetItem()
                first_buy_price = QTableWidgetItem()
                current_cost_price = QTableWidgetItem()
                number_of_stock = QTableWidgetItem()
                current_market_value = QTableWidgetItem()
                win_percent = QTableWidgetItem()
                upper_percent = QTableWidgetItem()
                first_buy_date.setData(QtCore.Qt.DisplayRole, values_list[row][2])
                first_buy_price.setData(QtCore.Qt.DisplayRole, values_list[row][3])
                current_cost_price.setData(QtCore.Qt.DisplayRole, values_list[row][4])
                number_of_stock.setData(QtCore.Qt.DisplayRole, values_list[row][5])
                current_market_value.setData(QtCore.Qt.DisplayRole, values_list[row][6])
                win_percent.setData(QtCore.Qt.DisplayRole, values_list[row][7])
                upper_percent.setData(QtCore.Qt.DisplayRole, values_list[row][8])
                # self.holderlist.setItem(row, 0, QTableWidgetItem(values_list[row][0]))
                self.holderlist.setItem(row, 0, code)
                self.holderlist.setItem(row, 1, QTableWidgetItem(values_list[row][1]))
                self.holderlist.setItem(row, 2, QTableWidgetItem(values_list[row][2]))
                self.holderlist.setItem(row, 3, QTableWidgetItem(str(values_list[row][3])))
                self.holderlist.setItem(row, 4, QTableWidgetItem(str(values_list[row][4])))
                self.holderlist.setItem(row, 5, QTableWidgetItem(str(values_list[row][5])))
                self.holderlist.setItem(row, 6, current_market_value)
                self.holderlist.setItem(row, 7, win_percent)
                self.holderlist.setItem(row, 8, upper_percent)
            # self.refresh_list()
            # self.refresh_upper_percent()
            self.holderlist.blockSignals(False)
        except Exception as e:
            self.message.show_message(str(e))
            print(e)

    def add_stock(self):
        code = self.codeinput.text()
        try:
            # rowPosition = self.holderlist.rowCount()
            # self.holderlist.insertRow(rowPosition)
            df = pd.DataFrame(get_value('df_holdlist'))
            code_list = df['code'].values.tolist()
            all_code = pd.read_csv('name.csv')['ts_code'].values.tolist()
            try:
                if "." not in code:
                    code = get_stock_code(code)
                if code in code_list:
                    message = MessageBox()
                    message.show_message(str(code) + '已存在')
                    # self.holderlist.removeRow(rowPosition)
                    # self.add_stock()
                elif code not in all_code:
                    message = MessageBox()
                    message.show_message('该股票可能不存在存在')
                    # self.holderlist.removeRow(rowPosition)
                else:
                    self.stockinfo.show()

            except Exception as e:
                traceback.print_exc()
        except Exception as e:
            # self.message.show_message(str(e))
            traceback.print_exc()

    def add_code_rest(self,dateTime, price, num):
        try:
            code = self.codeinput.text()
            if "." not in code:
                code = get_stock_code(code)
            path = os.getcwd() + os.path.sep + 'hold_dir' + '\\' + code + '.csv'
            rowPosition = self.holderlist.rowCount()
            self.holderlist.insertRow(rowPosition)
            name = get_name(code)
            price_date = hold_stock(code)
            market_price = price_date[0] * num
            upper_percent = round((price_date[0] - price) * 100 / price, 2)
            all_principal = num * price
            now_principal = all_principal - num * price
            create_holdstock_csv(code)
            write_data = [dateTime,1,price,price,num,now_principal,all_principal,all_principal,0]
            write_to_csv(path,write_data)
            self.holderlist.blockSignals(True)
            self.holderlist.setItem(rowPosition, 0, QTableWidgetItem(str(code)))
            self.holderlist.setItem(rowPosition, 1, QTableWidgetItem(str(name)))
            self.holderlist.setItem(rowPosition, 2, QTableWidgetItem(str(dateTime)))
            self.holderlist.setItem(rowPosition, 3, QTableWidgetItem(str(price)))
            self.holderlist.setItem(rowPosition, 4, QTableWidgetItem(str(price)))
            self.holderlist.setItem(rowPosition, 5, QTableWidgetItem(str(num)))
            self.holderlist.setItem(rowPosition, 6, QTableWidgetItem(str(market_price)))
            self.holderlist.setItem(rowPosition, 7, QTableWidgetItem(str(0)))
            self.holderlist.setItem(rowPosition, 8, QTableWidgetItem(str(upper_percent)))
            self.holderlist.blockSignals(False)
            self.save()
        except Exception as e:
            traceback.print_exc()

    def save(self):
        path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'
        try:
            df = pd.DataFrame(get_value('df_holdlist'))
            row_count = self.holderlist.rowCount()
            col_count = self.holderlist.columnCount()
            content = []
            for row in range(row_count):
                row_content = []
                for col in range(col_count):
                    item = self.holderlist.item(row, col)
                    if item is not None:
                        row_content.append(item.text())
                    else:
                        row_content.append(item)
                df.loc[row] = row_content
                content.append(row_content)
            set_value('df_holdlist', df)
            df.to_csv(path, index=False)
            self.refresh()
            self.refresh_upper_percent()
        except Exception as e:
            traceback.print_exc()

    # 设置单元格不可编辑
    def set_unedit(self, col):
        self.holderlist.blockSignals(True)
        row_count = self.holderlist.rowCount()
        for row in range(row_count):
            text = self.holderlist.item(row, col).text()
            item = QtWidgets.QTableWidgetItem(text)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.holderlist.setItem(row, col, item)
        self.holderlist.blockSignals(False)

    # 设置单元格可编辑
    def set_editable(self):
        self.holderlist.blockSignals(True)
        row_count = self.holderlist.rowCount()
        item2 = QtWidgets.QTableWidgetItem()
        item2.setFlags(QtCore.Qt.ItemFlag(63))
        # text = self.holderlist.item(row, col).text()
        # item = QtWidgets.QTableWidgetItem(text)
        # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.holderlist.setItem(row_count, 0, item2)
        self.holderlist.blockSignals(False)

    def code_col_click(self):
        row_count = self.holderlist.rowCount()

    # 检测是否插入新的行
    def check(self,row,col):
        df = pd.DataFrame(get_value('df_holdlist'))
        code_list = df['code'].values.tolist()
        try:
            current_row = self.holderlist.currentRow()
            current_col = self.holderlist.currentColumn()
            if col == 5:
                number = self.holderlist.item(current_row,5).text()
                code = self.holderlist.item(current_row,0).text()
                price_date = hold_stock(code)
                current_maket_price = price_date[0] * int(number)
                self.holderlist.blockSignals(True)
                self.holderlist.setItem(current_row,6,QTableWidgetItem(str(current_maket_price)))
                self.holderlist.blockSignals(False)
                self.save()
        except Exception as e:
            self.message.show_message(str(e))
            traceback.print_exc()

    def delete(self):
        path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'
        try:
            df = pd.DataFrame(get_value('df_holdlist'))
            current_row_list = []
            code_list = []
            for i in range(len(self.holderlist.selectedItems())):
                row = self.holderlist.selectedItems()[i].row()
                current_row_list.append(row)
                code_list.append(self.holderlist.item(row, 0).text())
            for row in current_row_list[::-1]:
                self.holderlist.removeRow(row)
            for code in code_list:
                df_index = df[df['code'] == code].index.values
                df = df.drop(labels=df_index, axis=0)
                csv_path = os.getcwd() + os.path.sep + 'hold_dir' + '\\' + code + '.csv'
                if os.path.exists(csv_path):
                    os.remove(csv_path)
            set_value('df_holdlist', df)
            df.to_csv(path, index=False)
        except Exception as e:
            traceback.print_exc()

    def sort_by_column(self, index):
        try:
            if self.orderType == Qt.DescendingOrder:
                self.orderType = Qt.AscendingOrder
            else:
                self.orderType = Qt.DescendingOrder
            self.holderlist.sortItems(index, self.orderType)
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))
            print(e)



    def buy(self):
        try:
            df = pd.DataFrame(get_value('df_holdlist'))
            add_number = self.codeinput.text()
            if add_number == '':
                add_number = 0
            else:
                add_number = int(add_number)
            if add_number != 0:
                row = self.holderlist.currentRow()
                code = self.holderlist.item(row, 0).text()
                number = int(df[df['code'] == code].number_of_stock.values[0])
                after_add = number+add_number
                if after_add < 0:
                    self.message.show_message('超出数量限制')
                else:
                    path = os.getcwd() + os.path.sep + 'hold_dir' + '\\' + code + '.csv'
                    last_data = pd.read_csv(path).tail(1)
                    # print(last_data)
                    last_principal = float(last_data['now_principal'])
                    last_allprincipal = float(last_data['all_principal'])
                    last_costprincipal = float(last_data['cost_principal'])
                    price_date = hold_stock(code)
                    now_price = price_date[0]
                    trade_date = price_date[1]
                    if add_number > 0:
                        trade_type = 1
                        now_principal = last_principal - (add_number * now_price)
                        if now_principal >= 0:
                            all_principal = now_principal + (add_number * now_price)
                            cost_principal = last_costprincipal
                        else:
                            now_principal = 0
                            all_principal = after_add * now_price
                            cost_principal = last_costprincipal + add_number * now_price
                        cost_price = round((cost_principal-now_principal)/after_add,2)
                        win_percent = round((all_principal - cost_principal)*100/cost_principal,2)
                    elif add_number < 0:
                        trade_type = -1
                        add_number = abs(add_number)
                        now_principal = last_principal + add_number * now_price
                        all_principal = now_principal + after_add * now_price
                        cost_principal = last_costprincipal
                        cost_price = round((cost_principal - now_principal) / after_add, 2)
                        win_percent = round((all_principal - cost_principal) * 100 / cost_principal, 2)
                    write_data = [trade_date,trade_type,now_price,cost_price,after_add,now_principal,all_principal,cost_principal,win_percent]
                    write_to_csv(path,write_data)
                    self.holderlist.setItem(row, 4, QTableWidgetItem(str(cost_price)))
                    self.holderlist.setItem(row, 5, QTableWidgetItem(str(after_add)))
                    self.holderlist.setItem(row, 7, QTableWidgetItem(str(win_percent)))
                    set_value('df_holdlist', df)
                    self.save()
                    # self.refresh()
            # print(code,add_number,number)
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))
            print(e)

    def refresh_upper_percent(self):
        try:
            path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'
            df = pd.read_csv(path)
            # code_list = pd.read_csv(path)['code'].values.tolist()
            row_count = self.holderlist.rowCount()
            for row in range(0,row_count):
                code = self.holderlist.item(row,0).text()
                now_price = hold_stock(code)[0]
                data_index = df[df['code'] == code].index.values.tolist()[0]
                # print(data_index)
                buy_price = df.iloc[data_index]['first_buy_price']
                upper_percent =round((now_price - buy_price)*100/buy_price,2)
                self.holderlist.setItem(row, 8, QTableWidgetItem(str(upper_percent)))
                # print(buy_price)
            # self.save()
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))

    def refresh_list(self):
        try:
            list_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'

            df = pd.read_csv(list_path)
            code_list = df['code'].values.tolist()
            conditionrsi = self.rsi.text()
            stoploss = self.stoploss.text()
            downnotbuy_flag = self.downnotbuy.isChecked()
            customer_flag = True
            csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
                downnotbuy_flag) + '\\' + conditionrsi + stoploss + '\\' + 'finishedlist.csv'
            # result_csv = pd.read_csv(csv_path)
            # row_count = self.holderlist.rowCount()
            # print(result_csv)
            # for row in range(0,row_count):
            #     print(row)
            #     code = self.holderlist.item(row,0).text()
            #     data_index = result_csv[result_csv['code'] == code].index.values.tolist()[0]
            #     print(result_csv[result_csv['code'] == code].index.values.tolist())
            #     trade_type = result_csv.iloc[data_index]['trade_type']
            #     if 0 < trade_type < 3:
            #         self.holderlist.item(row, 0).setBackground(QBrush(QColor(181, 61, 61)))
            #     elif trade_type < 0 or trade_type == 3:
            #         self.holderlist.item(row, 0).setBackground(QBrush(QColor(74, 194, 194)))
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))
    def real_test(self):
        pass
        # try:
        #     print(1)
        #     processlist = []
        #     num = 2
        #     conditionrsi = float(self.rsi.text())
        #     stoploss = float(self.stoploss.text())
        #     downnotbuy_flag = self.downnotbuy.isChecked()
        #     customer_flag = True
        #     list_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'
        #     df = pd.read_csv(list_path)
        #     code_list = df['code'].values.tolist()
        #     splited_list = split_list_n_list(code_list, num)
        #     for item in splited_list:
        #         process = multiprocessing.Process(target=run, args=(
        #             item, conditionrsi, stoploss, downnotbuy_flag, 100000, -10000, customer_flag))
        #         processlist.append(process)
        #         process.start()
        #     thread1 = threading.Thread(target=check_process_running, args=(
        #     processlist, self, conditionrsi, stoploss, customer_flag, downnotbuy_flag,))
        #     thread1.start()
        # except Exception as e:
        #     message = MessageBox()
        #     message.show_message(str(e))

class HolderUI(QMainWindow, Ui_Holder):
    def __init__(self):
        super(HolderUI, self).__init__()
        self.setupUi(self)
        self.refresh()
        self.refresh_upper_percent()
        # self.set_unedit(0)


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None




