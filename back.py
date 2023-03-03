# -*- coding: utf-8 -*-
import csv
import datetime
import multiprocessing
import os
import shutil
import threading
import traceback

import pandas as pd
# Form implementation generated from reading ui file 'back.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QMainWindow, qApp, QStyleOptionButton, QStyle
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QRect
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QMessageBox, QMainWindow

from gol_all import get_value, set_value
from baseFun import split_list_n_list, set_kline_data, get_stock_code, get_name, mkdir, kill_proc_tree, create_all_dir, \
    get_need_data, get_path, check_process_running, pull_fun_name, pull_stock_name
from MessageBox import MessageBox, QuestionBox
from backtest_all import run2_all
from load_csvdata import load_finished_code, load_winning_code,load_today_buy
from buyandsellui import BuyandSell
from trade_strategy2 import run
# 用来装行表头所有复选框 全局变量
all_header_combobox = []


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1177, 724)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(100, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        # self.startday = QtWidgets.QLineEdit(self.groupBox)
        # self.startday.setMaximumSize(QtCore.QSize(16777215, 30))
        # self.startday.setObjectName("startday")
        # self.gridLayout.addWidget(self.startday, 0, 0, 1, 1)
        # self.endday = QtWidgets.QLineEdit(self.groupBox)
        # self.endday.setMaximumSize(QtCore.QSize(16777215, 30))
        # self.endday.setObjectName("endday")
        # self.gridLayout.addWidget(self.endday, 1, 0, 1, 1)
        self.conditionrsi = QtWidgets.QLineEdit(self.groupBox)
        self.conditionrsi.setMaximumSize(QtCore.QSize(16777215, 30))
        self.conditionrsi.setObjectName("conditionrsi")
        self.gridLayout.addWidget(self.conditionrsi, 2, 0, 1, 1)
        self.stoploss = QtWidgets.QLineEdit(self.groupBox)
        self.stoploss.setMaximumSize(QtCore.QSize(16777215, 30))
        self.stoploss.setObjectName("stoploss")
        self.gridLayout.addWidget(self.stoploss, 3, 0, 1, 1)
        self.processnum = QtWidgets.QLineEdit(self.groupBox)
        self.processnum.setMaximumSize(QtCore.QSize(16777215, 30))
        self.processnum.setObjectName("processnum")
        self.gridLayout.addWidget(self.processnum, 4, 0, 1, 1)
        self.winningpercent = QtWidgets.QLineEdit(self.groupBox)
        self.winningpercent.setMaximumSize(QtCore.QSize(16777215, 30))
        self.winningpercent.setObjectName("winningpercent")
        self.gridLayout.addWidget(self.winningpercent, 5, 0, 1, 1)
        self.principal = QtWidgets.QLineEdit(self.groupBox)
        self.principal.setMaximumSize(QtCore.QSize(16777215, 30))
        self.principal.setObjectName("principal")
        self.gridLayout.addWidget(self.principal, 6, 0, 1, 1)
        self.downnotbuy = QtWidgets.QCheckBox(self.groupBox)
        self.downnotbuy.setObjectName("downnotbuy")
        self.gridLayout.addWidget(self.downnotbuy, 7, 0, 1, 1)
        self.downnotbuy.setChecked(True)

        self.todaybuy = QtWidgets.QCheckBox(self.groupBox)
        self.todaybuy.setObjectName("todaybuy")
        self.gridLayout.addWidget(self.todaybuy, 8, 0, 1, 1)
        # self.todaybuy.setChecked(True)

        self.start = QtWidgets.QPushButton(self.groupBox)
        self.start.setObjectName("start")
        self.gridLayout.addWidget(self.start, 9, 0, 1, 1)
        self.refresh = QtWidgets.QPushButton(self.groupBox)
        self.refresh.setObjectName("refresh")
        self.gridLayout.addWidget(self.refresh, 10, 0, 1, 1)
        self.stop = QtWidgets.QPushButton(self.groupBox)
        self.stop.setObjectName("stop")
        self.gridLayout.addWidget(self.stop, 12, 0, 1, 1)
        self.clear = QtWidgets.QPushButton(self.groupBox)
        self.clear.setObjectName("clear")
        self.gridLayout.addWidget(self.clear, 13, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(100, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.finishedlist = QtWidgets.QListWidget(self.groupBox_2)
        self.finishedlist.setObjectName("finishedlist")
        self.verticalLayout.addWidget(self.finishedlist)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.satisfaciedlist = QtWidgets.QTableWidget(self.groupBox_3)
        self.satisfaciedlist.setObjectName("satisfaciedlist")
        self.satisfaciedlist.setColumnCount(0)
        self.satisfaciedlist.setRowCount(0)
        self.verticalLayout_2.addWidget(self.satisfaciedlist)
        self.addholder = QtWidgets.QPushButton(self.groupBox_3)
        self.addholder.setObjectName("addholder")
        self.verticalLayout_2.addWidget(self.addholder)
        self.addcustomer = QtWidgets.QPushButton(self.groupBox_3)
        self.addholder.setObjectName("addcustomer")
        self.verticalLayout_2.addWidget(self.addcustomer)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.satisfaciedlist.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.satisfaciedlist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.satisfaciedlist.setColumnCount(6)
        self.satisfaciedlist.setHorizontalHeaderLabels(['代码', '名称', '统计时间段', '收益率', '股票涨幅', '差异率'])
        self.satisfaciedlist.horizontalHeader().setSectionsClickable(True)
        self.satisfaciedlist.horizontalHeader().setSortIndicatorShown(True)
        self.orderType = Qt.AscendingOrder
        self.satisfaciedlist.setAlternatingRowColors(True)

        # self.startday.setPlaceholderText('开始日期')
        # self.endday.setPlaceholderText('结束日期')
        self.conditionrsi.setPlaceholderText('条件一rsi')
        self.stoploss.setPlaceholderText('止损率')
        self.processnum.setPlaceholderText('创建进程数')
        self.winningpercent.setPlaceholderText('收益率')
        self.principal.setPlaceholderText('资金')
        # self.code.setPlaceholderText('单只股票代码')

        today = datetime.datetime.today().strftime('%Y%m%d')
        # self.startday.setText('20220701')
        # self.endday.setText(today)
        self.conditionrsi.setText('0.1')
        self.stoploss.setText('0.2')
        self.processnum.setText('2')
        self.winningpercent.setText('0.1')
        self.principal.setText('100000')

        self.start.clicked.connect(self.select_run)
        self.refresh.clicked.connect(self.refresh_list)
        self.stop.clicked.connect(self.stop_run)
        self.satisfaciedlist.doubleClicked.connect(self.get_info)
        self.clear.clicked.connect(self.delete_dir)
        self.satisfaciedlist.horizontalHeader().sectionClicked.connect(self.sort_by_column)
        self.addholder.clicked.connect(self.add_to_holdlist)
        self.downnotbuy.clicked.connect(self.refresh_list)
        self.addcustomer.clicked.connect(self.add_customer)
        self.todaybuy.clicked.connect(self.today_buy)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "属性"))
        self.start.setText(_translate("MainWindow", "开始"))
        self.stop.setText(_translate("MainWindow", "停止"))
        self.refresh.setText(_translate("MainWindow", "刷新"))
        self.downnotbuy.setText(_translate("MainWindow", "MA下行不买入"))
        self.todaybuy.setText(_translate("MainWindow", "今日买入"))
        self.clear.setText(_translate("MainWindow", "清除"))
        self.groupBox_2.setTitle(_translate("MainWindow", "已回测"))
        self.groupBox_3.setTitle(_translate("MainWindow", "符合要求"))
        self.addholder.setText(_translate("MainWindow", "添加到持股列表"))
        self.addcustomer.setText(_translate("MainWindow", "添加到自定义回测"))

    def select_run(self):
        self.run()

    def run(self):
        try:
            processlist = []
            num = int(self.processnum.text())
            # startday = self.startday.text()
            # endday = self.endday.text()
            conditionrsi = float(self.conditionrsi.text())
            stoploss = float(self.stoploss.text())
            principal = int(self.principal.text())
            downnotbuy_flag = self.downnotbuy.isChecked()
            customer_flag = False
            percent = float(self.winningpercent.text())
            df = pd.concat([pull_stock_name(), pull_fun_name()], ignore_index=True)
            df['symbol'] = df['ts_code'].apply(lambda x: x[0:6])
            df.to_csv('name.csv')
            # code_list = sorted(list(
            #     set(df['ts_code'].values.tolist()) - set(
            #         load_finished_code(conditionrsi, stoploss, downnotbuy_flag, customer_flag))))
            code_list = df['ts_code'].values.tolist()
            splited_list = split_list_n_list(code_list, num)
            for item in splited_list:
                process = multiprocessing.Process(target=run, args=(
                    item, conditionrsi, stoploss,  downnotbuy_flag, principal,percent, customer_flag))
                processlist.append(process)
                process.start()
            thread1 = threading.Thread(target=check_process_running, args=(processlist, self,conditionrsi,stoploss,customer_flag,downnotbuy_flag,))
            thread1.start()
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))

    def refresh_list(self):
        row = 0
        # startday = self.startday.text()
        # endday = self.endday.text()
        conditionrsi = float(self.conditionrsi.text())
        stoploss = float(self.stoploss.text())
        percent = float(self.winningpercent.text())
        downnotbuy_flag = self.downnotbuy.isChecked()
        customer_flag = False
        try:
            finished_list = load_finished_code(conditionrsi, stoploss, downnotbuy_flag, customer_flag)
            satisfied_code_win_name = load_winning_code(conditionrsi, stoploss, percent,
                                                        downnotbuy_flag, customer_flag)
            self.finishedlist.clear()
            self.satisfaciedlist.setRowCount(len(satisfied_code_win_name))
            for finished_code in finished_list:
                self.finishedlist.addItem(finished_code)
            while row < len(satisfied_code_win_name):
                trade_type = satisfied_code_win_name[row][6]
                win = QTableWidgetItem()
                upper = QTableWidgetItem()
                diff = QTableWidgetItem()
                win.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][3])
                upper.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][4])
                diff.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][5])
                self.satisfaciedlist.setItem(row, 0, QTableWidgetItem(satisfied_code_win_name[row][0]))
                self.satisfaciedlist.setItem(row, 1, QTableWidgetItem(str(satisfied_code_win_name[row][1])))
                self.satisfaciedlist.setItem(row, 2, QTableWidgetItem(satisfied_code_win_name[row][2]))
                # self.satisfaciedlist.setItem(row, 3, QTableWidgetItem(str(satisfied_code_win_name[row][3])))
                self.satisfaciedlist.setItem(row, 3, win)
                self.satisfaciedlist.setItem(row, 4, upper)
                self.satisfaciedlist.setItem(row, 5, diff)
                if trade_type > 0:
                    self.satisfaciedlist.item(row, 0).setBackground(QBrush(QColor(181, 61, 61)))
                elif trade_type < 0:
                    self.satisfaciedlist.item(row, 0).setBackground(QBrush(QColor(74, 194, 194)))
                row = row + 1
            self.satisfaciedlist.sortItems(0, Qt.AscendingOrder)
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))

    def stop_run(self):
        me = os.getpid()
        try:
            kill_proc_tree(me)
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message('停止出错，请重试')

    def get_info(self):
        try:
            # startday = self.startday.text()
            # endday = self.endday.text()
            conditionrsi = float(self.conditionrsi.text())
            stoploss = float(self.stoploss.text())
            downnotbuy_flag = self.downnotbuy.isChecked()
            customer_flag = False
            row = self.satisfaciedlist.selectedItems()[0].row()  # 获取选中文本所在的行
            # print("所选的内容所在的行为：", row)
            column = self.satisfaciedlist.selectedItems()[0].column()  # 获取选中文本所在的列
            # print("所选的内容所在的列为：", column)
            contents = self.satisfaciedlist.selectedItems()[0].text()  # 获取选中文本内容
            # print("选择的内容为：", contents)

            if column == 0:
                saved_dir_path = os.getcwd() + os.path.sep + '\\' + 'saved_data'
                data_path = saved_dir_path + '\\' + contents.replace('.', '') + '.csv'
                # trade_info = get_need_data(data_path, startday, endday, 60, 10)
                trade_info = pd.read_csv(data_path)[-100:]
                trade_info['trade_date'] = pd.to_datetime(trade_info['trade_date'], format='%Y%m%d').apply(
                    lambda x: x.strftime('%Y-%m-%d'))
                csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(downnotbuy_flag) + '\\' + str(conditionrsi) + str(stoploss) + '\\' + contents + '.csv'
                url = get_path('multiHtml') + contents.replace('.', '') + '.html'
                details = pd.read_csv(csv_path).iloc[-60:]
                details = details[details['trade_type'] != 0]
                date_list = details['date'].values.tolist()
                buysell_list = details['trade_type'].values.tolist()
                trans_list = []
                trade_info = trade_info.set_index('trade_date')
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
                self.buyandsell = BuyandSell()
                self.buyandsell.tableWidget.setRowCount(len(details))
                for row in range(len(details)):
                    self.buyandsell.tableWidget.setItem(row, 0, QTableWidgetItem(str(date_list[row])))
                    self.buyandsell.tableWidget.setItem(row, 1, QTableWidgetItem(trans_list[row]))
                    self.buyandsell.tableWidget.setItem(row, 2, QTableWidgetItem(str(price_list[row])))
                self.buyandsell.browser.load(QUrl.fromLocalFile(url))
                self.buyandsell.show()
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))
            print(e)

    def delete_dir(self):
        message = QuestionBox()
        if message.show_question("确认要删除所有回测文件？"):
            dir_path_list = create_all_dir()
            for path in dir_path_list:
                try:
                    shutil.rmtree(path)
                except Exception as e:
                    continue
            create_all_dir()
        self.refresh_list()

    def sort_by_column(self, index):
        try:
            if self.orderType == Qt.DescendingOrder:
                self.orderType = Qt.AscendingOrder
            else:
                self.orderType = Qt.DescendingOrder
            self.satisfaciedlist.sortItems(index, self.orderType)
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))
            print(e)

    def add_to_holdlist(self):
        """
        选中股票加入持股列表
        :return:
        """
        try:
            add_row = []
            df = pd.DataFrame(get_value('df_holdlist'))
            exsist_list = df['code'].values.tolist()
            warn_list = []
            for i in range(len(self.satisfaciedlist.selectedItems())):
                row = self.satisfaciedlist.selectedItems()[i].row()  # 获取选中文本所在的行
                code = self.satisfaciedlist.item(row, 0).text()
                name = self.satisfaciedlist.item(row, 1).text()
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
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))
            print(e)

    def keyPressEvent(self, event):
        """ Ctrl + C复制表格内容 """
        try:
            if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                # 获取表格的选中行
                selected_ranges = self.satisfaciedlist.selectedRanges()[0]
                text_str = ""  # 最后总的内容
                # 行（选中的行信息读取）
                for row in range(selected_ranges.topRow(), selected_ranges.bottomRow() + 1):
                    row_str = ""
                    # 列（选中的列信息读取）
                    for col in range(selected_ranges.leftColumn(), selected_ranges.rightColumn() + 1):
                        item = self.satisfaciedlist.item(row, col)
                        row_str += item.text() + '\t'  # 制表符间隔数据
                    text_str += row_str + '\n'  # 换行
                clipboard = qApp.clipboard()  # 获取剪贴板
                clipboard.setText(text_str)  # 内容写入剪贴板
        except Exception as e:
            traceback.print_exc()


    def add_customer(self):
        try:
            csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'custmoerlist.csv'
            df = pd.read_csv(csv_path)
            df_code_list = df['code'].values.tolist()
            for i in range(len(self.satisfaciedlist.selectedItems())):
                row = self.satisfaciedlist.selectedItems()[i].row()  # 获取选中文本所在的行
                code = self.satisfaciedlist.item(row,0).text()
                if code not in df_code_list:
                    name = get_name(code)
                    df.loc[len(df)] = [code,name]
            df.to_csv(csv_path, index=False, encoding="utf-8")
        except Exception as e:
            traceback.print_exc()
            message = MessageBox()
            message.show_message(str(e))

    def today_buy(self):
        todaybuy_falg = self.todaybuy.isChecked()
        if not todaybuy_falg:
            self.refresh_list()
        else:
            row = 0
            # startday = self.startday.text()
            # endday = self.endday.text()
            conditionrsi = float(self.conditionrsi.text())
            stoploss = float(self.stoploss.text())
            percent = float(self.winningpercent.text())
            downnotbuy_flag = self.downnotbuy.isChecked()
            customer_flag = False
            try:
                satisfied_code_win_name = load_today_buy(conditionrsi, stoploss,downnotbuy_flag)
                self.satisfaciedlist.setRowCount(len(satisfied_code_win_name))
                while row < len(satisfied_code_win_name):
                    win = QTableWidgetItem()
                    upper = QTableWidgetItem()
                    diff = QTableWidgetItem()
                    win.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][3])
                    upper.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][4])
                    diff.setData(QtCore.Qt.DisplayRole, satisfied_code_win_name[row][5])
                    self.satisfaciedlist.setItem(row, 0, QTableWidgetItem(satisfied_code_win_name[row][0]))
                    self.satisfaciedlist.setItem(row, 1, QTableWidgetItem(str(satisfied_code_win_name[row][1])))
                    self.satisfaciedlist.setItem(row, 2, QTableWidgetItem(satisfied_code_win_name[row][2]))
                    # self.satisfaciedlist.setItem(row, 3, QTableWidgetItem(str(satisfied_code_win_name[row][3])))
                    self.satisfaciedlist.setItem(row, 3, win)
                    self.satisfaciedlist.setItem(row, 4, upper)
                    self.satisfaciedlist.setItem(row, 5, diff)
                    self.satisfaciedlist.item(row, 0).setBackground(QBrush(QColor(181, 61, 61)))
                    row = row + 1
                self.satisfaciedlist.sortItems(0, Qt.AscendingOrder)
            except Exception as e:
                traceback.print_exc()
                message = MessageBox()
                message.show_message(str(e))

class Backall_resize(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Backall_resize, self).__init__()
        self.setupUi(self)
        self.refresh_list()
