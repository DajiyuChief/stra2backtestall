# -*- coding: utf-8 -*-
import csv
import datetime
import multiprocessing
import os
import shutil
import traceback
import threading

import pandas as pd
# Form implementation generated from reading ui file 'customer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, qApp

from MessageBox import MessageBox, QuestionBox
from backtest_all import run2_all
from baseFun import get_stock_code, get_name, split_list_n_list, mkdir, kill_proc_tree, get_need_data, set_kline_data, \
    create_customer_dir, find_proc_tree, check_process_running
from buyandsellui import BuyandSell
from gol_all import get_value, set_value
from load_csvdata import load_finished_code, load_winning_code
from trade_strategy2 import run


class Ui_customer(object):
    def setupUi(self, customer):
        customer.setObjectName("customer")
        customer.resize(1079, 830)
        self.horizontalLayout = QtWidgets.QHBoxLayout(customer)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(customer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(100, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # self.startday = QtWidgets.QLineEdit(self.groupBox)
        # self.startday.setMaximumSize(QtCore.QSize(16777215, 35))
        # self.startday.setObjectName("startday")
        # self.verticalLayout_2.addWidget(self.startday)
        # self.endday = QtWidgets.QLineEdit(self.groupBox)
        # self.endday.setMaximumSize(QtCore.QSize(16777215, 35))
        # self.endday.setObjectName("endday")
        # self.verticalLayout_2.addWidget(self.endday)
        self.conditionrsi = QtWidgets.QLineEdit(self.groupBox)
        self.conditionrsi.setMaximumSize(QtCore.QSize(16777215, 35))
        self.conditionrsi.setObjectName("conditionrsi")
        self.verticalLayout_2.addWidget(self.conditionrsi)
        self.stoploss = QtWidgets.QLineEdit(self.groupBox)
        self.stoploss.setMaximumSize(QtCore.QSize(16777215, 35))
        self.stoploss.setObjectName("stoploss")
        self.verticalLayout_2.addWidget(self.stoploss)
        self.processnum = QtWidgets.QLineEdit(self.groupBox)
        self.processnum.setMaximumSize(QtCore.QSize(16777215, 35))
        self.processnum.setObjectName("processnum")
        self.verticalLayout_2.addWidget(self.processnum)
        self.principal = QtWidgets.QLineEdit(self.groupBox)
        self.principal.setMaximumSize(QtCore.QSize(16777215, 35))
        self.principal.setObjectName("principal")
        self.verticalLayout_2.addWidget(self.principal)
        self.downnotbuy = QtWidgets.QCheckBox(self.groupBox)
        self.downnotbuy.setChecked(True)
        self.downnotbuy.setObjectName("downnotbuy")
        self.verticalLayout_2.addWidget(self.downnotbuy)
        self.start = QtWidgets.QPushButton(self.groupBox)
        self.start.setObjectName("start")
        self.verticalLayout_2.addWidget(self.start)
        self.refresh = QtWidgets.QPushButton(self.groupBox)
        self.refresh.setObjectName("refresh")
        self.verticalLayout_2.addWidget(self.refresh)
        self.stop = QtWidgets.QPushButton(self.groupBox)
        self.stop.setObjectName("stop")
        self.verticalLayout_2.addWidget(self.stop)
        self.clear = QtWidgets.QPushButton(self.groupBox)
        self.clear.setObjectName("clear")
        self.verticalLayout_2.addWidget(self.clear)
        self.todaytestbutton = QtWidgets.QPushButton(self.groupBox)
        self.todaytestbutton.setObjectName("todaytestbutton")
        self.verticalLayout_2.addWidget(self.todaytestbutton)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(customer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(100, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.customerlist = QtWidgets.QTableWidget(self.groupBox_2)
        self.customerlist.setObjectName("customerlist")
        self.customerlist.setColumnCount(2)
        self.customerlist.setRowCount(0)
        self.verticalLayout.addWidget(self.customerlist)
        self.codeinput = QtWidgets.QTextEdit(self.groupBox_2)
        self.codeinput.setMaximumSize(QtCore.QSize(16777215, 40))
        self.codeinput.setObjectName("codeinput")
        self.verticalLayout.addWidget(self.codeinput)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addbutton = QtWidgets.QPushButton(self.groupBox_2)
        self.addbutton.setObjectName("addbutton")
        self.horizontalLayout_2.addWidget(self.addbutton)
        self.deletebutton = QtWidgets.QPushButton(self.groupBox_2)
        self.deletebutton.setObjectName("deletebutton")
        self.horizontalLayout_2.addWidget(self.deletebutton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(customer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.outputtable = QtWidgets.QTableWidget(self.groupBox_3)
        self.outputtable.setObjectName("outputtable")
        self.outputtable.setColumnCount(6)
        self.outputtable.setRowCount(0)
        self.verticalLayout_4.addWidget(self.outputtable)
        self.addholderbutton = QtWidgets.QPushButton(self.groupBox_3)
        self.addholderbutton.setObjectName("addholderbutton")
        self.verticalLayout_4.addWidget(self.addholderbutton)
        self.horizontalLayout.addWidget(self.groupBox_3)

        # self.startday.setTabChangesFocus(True)
        # self.endday.setTabChangesFocus(True)
        # self.conditionrsi.setTabChangesFocus(True)
        # self.stoploss.setTabChangesFocus(True)
        # self.processnum.setTabChangesFocus(True)
        # self.principal.setTabChangesFocus(True)
        self.codeinput.setTabChangesFocus(False)
        self.customerlist.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.customerlist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.customerlist.setHorizontalHeaderLabels(['代码', '名称'])
        self.outputtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.outputtable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.outputtable.setHorizontalHeaderLabels(['代码', '名称', '统计时间段', '收益率', '股票涨幅', '差异率'])
        self.outputtable.horizontalHeader().setSectionsClickable(True)
        self.outputtable.horizontalHeader().setSortIndicatorShown(True)
        self.orderType = Qt.AscendingOrder
        self.outputtable.setAlternatingRowColors(True)

        self.addbutton.clicked.connect(self.add_code)
        self.deletebutton.clicked.connect(self.delete_selected)
        self.start.clicked.connect(self.run_customer)
        self.refresh.clicked.connect(self.refresh_list)
        self.stop.clicked.connect(self.stop_run)
        self.clear.clicked.connect(self.delete_dir)
        self.addholderbutton.clicked.connect(self.add_to_holdlist)
        self.outputtable.doubleClicked.connect(self.get_info)
        self.outputtable.horizontalHeader().sectionClicked.connect(self.sort_by_column)
        self.downnotbuy.clicked.connect(self.refresh_list)
        self.todaytestbutton.clicked.connect(self.run_customer)

        # self.startday.setPlaceholderText('开始日期')
        # self.endday.setPlaceholderText('结束日期')
        self.conditionrsi.setPlaceholderText('条件一rsi')
        self.stoploss.setPlaceholderText('止损率')
        self.processnum.setPlaceholderText('创建进程数')
        self.principal.setPlaceholderText('资金')
        today = datetime.datetime.today().strftime('%Y%m%d')
        # self.startday.setText('20220701')
        # self.endday.setText(today)
        self.conditionrsi.setText('0.1')
        self.stoploss.setText('0.2')
        self.processnum.setText('2')
        self.principal.setText('100000')

        self.retranslateUi(customer)
        QtCore.QMetaObject.connectSlotsByName(customer)

    def retranslateUi(self, customer):
        _translate = QtCore.QCoreApplication.translate
        customer.setWindowTitle(_translate("customer", "Form"))
        self.groupBox.setTitle(_translate("customer", "属性"))
        self.downnotbuy.setText(_translate("customer", "MA下行不买入"))
        self.start.setText(_translate("customer", "开始"))
        self.refresh.setText(_translate("customer", "刷新"))
        self.stop.setText(_translate("customer", "停止"))
        self.clear.setText(_translate("customer", "清除"))
        self.groupBox_2.setTitle(_translate("customer", "回测列表"))
        self.addbutton.setText(_translate("customer", "添加"))
        self.deletebutton.setText(_translate("customer", "删除"))
        self.groupBox_3.setTitle(_translate("customer", "回测结果"))
        self.addholderbutton.setText(_translate("customer", "添加到持股列表"))
        self.todaytestbutton.setText(_translate("customer", "今日测试"))

    def add_code(self):
        try:
            exist_list = []
            csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'custmoerlist.csv'
            df = pd.read_csv(csv_path)
            code_list = df['code'].values.tolist()
            code = self.codeinput.toPlainText()
            code_input_list = code.split('\n')
            while '' in code_input_list:
                code_input_list.remove('')
            for item in code_input_list:
                code = get_stock_code(item)
                if code in code_list:
                    exist_list.append(code)
                    continue
                name = get_name(code)
                with open(csv_path, 'a',
                          encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([code, name])
            self.refresh_customer_lsit()
            if len(exist_list) > 0:
                exist_code = ','.join(exist_list)
                message = MessageBox()
                message.show_message(exist_code + '已存在，请勿重复添加')
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))

    def refresh_customer_lsit(self):
        csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'custmoerlist.csv'
        df = pd.read_csv(csv_path)
        df_list = df.values.tolist()
        self.customerlist.setRowCount(len(df))
        for i in range(len(df)):
            self.customerlist.setItem(i, 0, QTableWidgetItem(str(df_list[i][0])))
            self.customerlist.setItem(i, 1, QTableWidgetItem(str(df_list[i][1])))

    def delete_selected(self):
        try:
            drop_row = []
            csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'custmoerlist.csv'
            df = pd.read_csv(csv_path)
            for i in range(len(self.customerlist.selectedItems())):
                row = self.customerlist.selectedItems()[i].row()  # 获取选中文本所在的行
                # column = self.customerlist.selectedItems()[i].column()  # 获取选中文本所在的列
                # contents = self.customerlist.selectedItems()[i].text()  # 获取选中文本内容
                drop_row.append(row)
                # print("选择的内容为：", contents)
                # print("所选的内容所在的行为：", row)
                # print("所选的内容所在的列为：", column)
            df = df.drop(drop_row)
            df.to_csv(csv_path, index=False, encoding="utf-8")
            self.refresh_customer_lsit()
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))

    def run_customer(self):
        try:
            processlist = []
            num = int(self.processnum.text())
            # startday = self.startday.text()
            # endday = self.endday.text()
            conditionrsi = float(self.conditionrsi.text())
            stoploss = float(self.stoploss.text())
            principal = int(self.principal.text())
            downnotbuy_flag = self.downnotbuy.isChecked()
            customer_flag = True
            list_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'custmoerlist.csv'
            df = pd.read_csv(list_path)
            # code_list = sorted(list(
            #     set(df['code'].values.tolist()) - set(
            #         load_finished_code(conditionrsi, stoploss, downnotbuy_flag, customer_flag))))
            code_list = df['code'].values.tolist()
            splited_list = split_list_n_list(code_list, num)
            for item in splited_list:
                process = multiprocessing.Process(target=run, args=(
                    item, conditionrsi, stoploss, downnotbuy_flag, principal, -10000, customer_flag))
                processlist.append(process)
                process.start()
            thread1 = threading.Thread(target=check_process_running, args=(
            processlist, self, conditionrsi, stoploss, customer_flag, downnotbuy_flag,))
            thread1.start()
        except Exception as e:
            message = MessageBox()
            message.show_message(str(e))

    def refresh_list(self):
        row = 0
        # startday = self.startday.text()
        # endday = self.endday.text()
        conditionrsi = float(self.conditionrsi.text())
        stoploss = float(self.stoploss.text())
        percent = float(0.1)
        downnotbuy_flag = self.downnotbuy.isChecked()
        customer_flag = True
        self.refresh_customer_lsit()
        try:

            satisfied_code_win_name = load_winning_code(conditionrsi, stoploss, percent,
                                                        downnotbuy_flag, customer_flag)
            self.outputtable.setRowCount(len(satisfied_code_win_name))
            while row < len(satisfied_code_win_name):
                trade_type = satisfied_code_win_name[row][6]
                win = QTableWidgetItem()
                upper = QTableWidgetItem()
                diff = QTableWidgetItem()
                win.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][3])
                upper.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][4])
                diff.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][5])
                self.outputtable.setItem(row, 0, QTableWidgetItem(satisfied_code_win_name[row][0]))
                self.outputtable.setItem(row, 1, QTableWidgetItem(str(satisfied_code_win_name[row][1])))
                self.outputtable.setItem(row, 2, QTableWidgetItem(satisfied_code_win_name[row][2]))
                self.outputtable.setItem(row, 3, win)
                self.outputtable.setItem(row, 4, upper)
                self.outputtable.setItem(row, 5, diff)
                if trade_type > 0:
                    self.outputtable.item(row, 0).setBackground(QBrush(QColor(181, 61, 61)))
                elif trade_type < 0:
                    self.outputtable.item(row, 0).setBackground(QBrush(QColor(74, 194, 194)))
                row = row + 1
        except Exception as e:
            message = MessageBox()
            message.show_message(str(e))

    def stop_run(self):
        me = os.getpid()
        try:
            kill_proc_tree(me)
        except Exception as e:
            message = MessageBox()
            message.show_message('停止出错，请重试')

    def get_info(self):
        try:
            # startday = self.startday.text()
            # endday = self.endday.text()
            conditionrsi = float(self.conditionrsi.text())
            stoploss = float(self.stoploss.text())
            downnotbuy_flag = self.downnotbuy.isChecked()
            customer_flag = True
            row = self.outputtable.selectedItems()[0].row()  # 获取选中文本所在的行
            column = self.outputtable.selectedItems()[0].column()  # 获取选中文本所在的列
            contents = self.outputtable.selectedItems()[0].text()  # 获取选中文本内容
            if column == 0:
                saved_dir_path = os.getcwd() + os.path.sep + '\\' + 'saved_data'
                data_path = saved_dir_path + '\\' + contents.replace('.', '') + '.csv'
                # trade_info = get_need_data(data_path, startday, endday, 60, 10)
                trade_info = pd.read_csv(data_path)[-100:]
                trade_info['trade_date'] = pd.to_datetime(trade_info['trade_date'], format='%Y%m%d').apply(
                    lambda x: x.strftime('%Y-%m-%d'))
                csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
                    downnotbuy_flag) + '\\' + str(conditionrsi) + str(stoploss) + '\\' + contents + '.csv'
                details = pd.read_csv(csv_path).iloc[-60:]
                details = details[details['trade_type'] != 0]
                date_list = details['date'].values.tolist()
                buysell_list = details['trade_type'].values.tolist()
                trans_list = []
                trade_info = trade_info.set_index('trade_date')
                url = os.getcwd() + os.path.sep + 'customer' + '\\' + 'generate_html' + '\\' + contents.replace('.',
                                                                                                                '') + '.html'
                set_kline_data(contents, details, trade_info, url)
                for type in buysell_list:
                    if type == 1:
                        trans_list.append('买')
                    elif type == 2:
                        trans_list.append('加')
                    elif type == 3:
                        trans_list.append('止盈')
                    elif type == -1:
                        trans_list.append('卖')
                    elif type == -2:
                        trans_list.append('减')
                    elif type == -3:
                        trans_list.append('止损')

                price_list = details['close'].values.tolist()
                # principal_list = details['principal'].values.tolist()
                self.buyandsell = BuyandSell()
                self.buyandsell.tableWidget.setRowCount(len(details))
                for row in range(len(details)):
                    self.buyandsell.tableWidget.setItem(row, 0, QTableWidgetItem(str(date_list[row])))
                    self.buyandsell.tableWidget.setItem(row, 1, QTableWidgetItem(trans_list[row]))
                    self.buyandsell.tableWidget.setItem(row, 2, QTableWidgetItem(str(price_list[row])))
                    # self.buyandsell.tableWidget.setItem(row, 3, QTableWidgetItem(str(principal_list[row])))
                self.buyandsell.browser.load(QUrl.fromLocalFile(url))
                self.buyandsell.show()
        except Exception as e:
            message = MessageBox()
            message.show_message(str(e))
            print(e)

    def delete_dir(self):
        message = QuestionBox()
        if message.show_question("确认要删除所有自定义回测文件？"):
            dir_path_list = create_customer_dir()
            for path in dir_path_list:
                try:
                    shutil.rmtree(path)
                except Exception as e:
                    continue
            create_customer_dir()
        self.refresh_list()

    def sort_by_column(self, index):
        try:
            if self.orderType == Qt.DescendingOrder:
                self.orderType = Qt.AscendingOrder
            else:
                self.orderType = Qt.DescendingOrder
            self.outputtable.sortItems(index, self.orderType)
        except Exception as e:
            message = MessageBox()
            message.show_message(str(e))
            print(e)

    def add_to_holdlist(self):
        try:
            add_row = []
            df = pd.DataFrame(get_value('df_holdlist'))
            exsist_list = df['code'].values.tolist()
            warn_list = []
            for i in range(len(self.outputtable.selectedItems())):
                row = self.outputtable.selectedItems()[i].row()  # 获取选中文本所在的行
                code = self.outputtable.item(row, 0).text()
                name = self.outputtable.item(row, 1).text()
                if code not in exsist_list:
                    add_row.append([code, name, '', '', '', '', '', '', ''])
                else:
                    warn_list.append(code)
            holdlist_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'
            for i in range(len(add_row)):
                df.loc[len(df)] = add_row[i]
            set_value('df_holdlist', df)
            df.to_csv(holdlist_path, index=False, encoding="utf-8")
            if len(warn_list) != 0:
                message = MessageBox()
                message.show_message(str(warn_list) + '已存在')
        except Exception as e:
            message = MessageBox()
            message.show_message(str(e))
            print(e)

    def keyPressEvent(self, event):
        """ Ctrl + C复制表格内容 """
        try:
            if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                # 获取表格的选中行
                selected_ranges = self.outputtable.selectedRanges()[0]
                text_str = ""  # 最后总的内容
                # 行（选中的行信息读取）
                for row in range(selected_ranges.topRow(), selected_ranges.bottomRow() + 1):
                    row_str = ""
                    # 列（选中的列信息读取）
                    for col in range(selected_ranges.leftColumn(), selected_ranges.rightColumn() + 1):
                        item = self.outputtable.item(row, col)
                        row_str += item.text() + '\t'  # 制表符间隔数据
                    text_str += row_str + '\n'  # 换行
                clipboard = qApp.clipboard()  # 获取剪贴板
                clipboard.setText(text_str)  # 内容写入剪贴板
        except Exception as e:
            traceback.print_exc()



class Customer(QWidget, Ui_customer):
    def __init__(self):
        super(Customer, self).__init__()
        self.setupUi(self)
        self.refresh_list()
