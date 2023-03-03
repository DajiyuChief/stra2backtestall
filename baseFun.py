# 记录公共函数
import csv
import datetime
import os
import time

import numpy as np
import tushare as ts
import pandas as pd
import psutil
import mysql.connector
from kline import plot_kline

pro = ts.pro_api('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
data = pro.query('trade_cal', start_date='20210101', end_date=datetime.date.today().strftime("%Y%m%d"), is_open='1')
date_list = list(data['cal_date'])[::-1]
date_int_list = list(map(int, date_list))


def setdata(start_day, end_day, stock_code):
    try:
        df = pro.daily(ts_code=stock_code, start_date=start_day, end_date=end_day)
        if len(df) == 0:
            df = pro.fund_daily(ts_code=stock_code, start_date=start_day, end_date=end_day)
    except:
        df = []
    df = df.sort_values(by='trade_date', ascending=True)
    return df


def save_trade_date():
    # 获取交易日
    data = pro.query('trade_cal', is_open='1')
    date_list = list(data['cal_date'])
    date_int_list = list(map(int, date_list))
    path = os.getcwd() + os.path.sep + 'date_list'
    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(date_int_list)
    return date_list, date_int_list


def split_list_n_list(origin_list, n):
    if len(origin_list) % n == 0:
        cnt = len(origin_list) // n
    else:
        cnt = len(origin_list) // n + 1

    for i in range(0, n):
        yield origin_list[i * cnt:(i + 1) * cnt]


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    # if including_parent:
    #     parent.kill()


def find_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        print(child.pid)


def mkdir(path):
    import os  # 用于创建文件夹
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在 true
    # 不存在 false
    isExits = os.path.exists(path)

    # 判断结果
    if not isExits:
        os.makedirs(path)  # 不存在则创建该目录
        return True


def set_kline_data(code, details, trade_info, url):
    buy = []
    sell = []
    add = []
    minus = []
    stopwin = []
    stoploss = []
    buy_high = []
    sell_high = []
    name = get_name(code)
    buy_date = details[details['trade_type'] == 1]['date'].values.tolist()
    sell_date = details[details['trade_type'] == -1]['date'].values.tolist()
    add_date = details[details['trade_type'] == 2]['date'].values.tolist()
    minus_date = details[details['trade_type'] == -2]['date'].values.tolist()
    stopwin_date = details[details['trade_type'] == 3]['date'].values.tolist()
    stoploss_date = details[details['trade_type'] == -3]['date'].values.tolist()
    buy_high = details[details['trade_type'] == 1]['high'].values.tolist()
    sell_high = details[details['trade_type'] == -1]['high'].values.tolist()
    add_high = details[details['trade_type'] == 2]['high'].values.tolist()
    minus_high = details[details['trade_type'] == -2]['high'].values.tolist()
    stopwin_high = details[details['trade_type'] == 3]['high'].values.tolist()
    stoploss_high = details[details['trade_type'] == -3]['high'].values.tolist()
    for item in buy_date:
        buy.append(datetime.datetime.strptime(str(item), '%Y%m%d').strftime('%Y-%m-%d'))
    for item in sell_date:
        sell.append(datetime.datetime.strptime(str(item), '%Y%m%d').strftime('%Y-%m-%d'))
    for item in add_date:
        add.append(datetime.datetime.strptime(str(item), '%Y%m%d').strftime('%Y-%m-%d'))
    for item in minus_date:
        minus.append(datetime.datetime.strptime(str(item), '%Y%m%d').strftime('%Y-%m-%d'))
    for item in stopwin_date:
        stopwin.append(datetime.datetime.strptime(str(item), '%Y%m%d').strftime('%Y-%m-%d'))
    for item in stoploss_date:
        stoploss.append(datetime.datetime.strptime(str(item), '%Y%m%d').strftime('%Y-%m-%d'))

    # grid = plot_kline_volume_signal(trade_info, name, [buy, buy_high, sell, sell_high])
    kline = plot_kline(trade_info, name,
                       [buy, buy_high, sell, sell_high, add, add_high, minus, minus_high, stopwin, stopwin_high,
                        stoploss, stoploss_high])
    # url = 'generate_html' + '\\' + code.replace('.', '') + '.html'
    # grid.render(url)
    kline.render(url)


def pull_stock_name():
    # 拉取股票数据
    df = pro.stock_basic(**{
        "ts_code": "",
        "name": "",
        "exchange": "",
        "market": "",
        "is_hs": "",
        "list_status": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "name"
    ])
    return df


def pull_fun_name():
    df = pro.fund_basic(market='E')
    df2 = df[['ts_code', 'name']]
    return df2


def get_name(stockcode):
    # 从表中获取姓名
    try:
        df = pd.read_csv('name.csv')
        if "." in stockcode:
            data = df[df['ts_code'] == stockcode]
            name = data['name'].values[0]
        else:
            data = df[df['ts_code'] == get_stock_code(int(stockcode))]
            name = data['name'].values[0]
        return name
    except:
        return stockcode


def get_stock_code(symbol):
    try:
        df = pd.read_csv('name.csv')
        if '.' not in symbol:
            data = df[df['symbol'] == int(symbol)]
            code = data['ts_code'].values[0]
        elif '.' in symbol:
            data = df[df['ts_code'] == symbol]
            code = data['ts_code'].values[0]
        return code
    except:
        print('可能在库中没有找到匹配的股票代码，请重试')


def find_real_start_end(start, end):
    global date_int_list
    # data = pro.query('trade_cal', start_date=start, end_date=end, is_open='1')
    # date_list = list(data['cal_date'])
    arr = np.array(date_int_list)
    # print(date_int_list)
    if int(start) not in date_int_list:
        start = arr[arr >= int(start)][0]
    if int(end) not in date_int_list:
        end = arr[arr <= int(end)][-1]
    list1 = date_list[date_int_list.index(int(start)):date_int_list.index(int(end)) + 1]
    return list1


# 从数据中切取需要的数据 参数为 csv路径，开始日期，结束日期，往前推时间 往后时间
def get_need_data(path, start, end, forworddays, backdays):
    df = pd.read_csv(path)
    date_list = find_real_start_end(start, end)
    start = int(date_list[0])
    end = int(date_list[-1])
    start_index = df[df['trade_date'] == start].index.tolist()[0]
    end_index = df[df['trade_date'] == end].index.tolist()[0] + 1
    if start_index >= forworddays:
        start_index = start_index - forworddays
    else:
        start_index = 0
    if end_index + backdays <= len(df):
        end_index = end_index + backdays
    else:
        end_index = len(df)
    return df.iloc[start_index:end_index]


def create_all_dir():
    dir_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(True)
    dir_path1 = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(False)
    # dir_path2 = os.getcwd() + os.path.sep + 'customer' + str(False)
    # dir_path3 = os.getcwd() + os.path.sep + 'customer' + str(True)
    dir_path5 = os.getcwd() + os.path.sep + 'multi' + '\\' + 'generate_html'
    # dir_path6 = os.getcwd() + os.path.sep + 'customer'
    dir_path_list = [dir_path, dir_path1, dir_path5]
    for path in dir_path_list:
        mkdir(path)
    return dir_path_list


def create_customer_dir():
    dir_path2 = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(False)
    dir_path3 = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(True)
    dir_path5 = os.getcwd() + os.path.sep + 'customer' + '\\' + 'generate_html'
    dir_path_list = [dir_path2, dir_path3, dir_path5]
    for path in dir_path_list:
        mkdir(path)
    return dir_path_list


def create_csv():
    list1_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'custmoerlist.csv'
    list2_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'holdlist.csv'
    # list3_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(True) + '\\' + 'finishedlist.csv'
    # list4_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(False) + '\\' + 'finishedlist.csv'
    # list5_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(False) + '\\' + 'finishedlist.csv'
    # list6_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(True) + '\\' + 'finishedlist.csv'
    header1 = ['code', 'name']
    header2 = ['code', 'name', 'first_buy_date', 'first_buy_price', 'current_cost_price', 'number_of_stock',
               'current_market_value', 'win_percnet', 'up_percent']
    header3 = ['code']
    header4 = ['code', 'priority']
    if not os.path.exists(list1_path):
        with open(list1_path, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header1)
    if not os.path.exists(list2_path):
        with open(list2_path, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header2)
    # for path in [list3_path,list4_path,list5_path,list6_path]:
    #     if not os.path.exists(path):
    #         with open(path, 'a', encoding='UTF8', newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow(header3)
    if not os.path.exists('priority.csv'):
        with open('priority.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header4)


def write_to_csv(path, content):
    with open(path, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        print()
        writer.writerow(content)


def create_finished_list(path):
    header = ['code', 'name', 'span', 'win_percent', 'up_percent', 'diff_percent', 'trade_type']
    if not os.path.exists(path):
        with open(path, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)


def connect_database(address, port, user, password):
    mydb = mysql.connector.connect(
        host=str(address),
        port=int(port),
        user=str(user),
        passwd=str(password)
    )
    cursor = mydb.cursor()
    return cursor
    # cursor.execute("show databases")


def check_process_running(process_list, window,rsi,stoploss,iscustomer,downnotbuy):
    if not iscustomer:
        dirpath = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(downnotbuy) + '\\' + str(rsi) + str(
            stoploss) + '\\'
        finishlist_path = dirpath + 'finishedlist.csv'
    else:
        dirpath = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(downnotbuy) + '\\' + str(
            rsi) + str(
            stoploss) + '\\'
        finishlist_path = dirpath + 'finishedlist.csv'
    while True:
        is_alive_flag = []
        for item in process_list:
            is_alive_flag.append(item.is_alive())
        if True in is_alive_flag:
            window.refresh_list()
            time.sleep(2)
        else:
            finishlist_csv = pd.read_csv(finishlist_path).drop_duplicates(subset='code', keep='last')
            finishlist_csv.to_csv(finishlist_path, index=False)
            window.refresh_list()
            break


def get_path(dir):
    if dir == 'customerFalse':
        return os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(False) + '\\'
    if dir == 'customerTrue':
        return os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(True) + '\\'
    if dir == 'multiFalse':
        return os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(False) + '\\'
    if dir == 'multiTrue':
        return os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(True) + '\\'
    if dir == 'multiHtml':
        return os.getcwd() + os.path.sep + 'multi' + '\\' + 'generate_html' + '\\'
    if dir == 'customerHtml':
        return os.getcwd() + os.path.sep + 'customer' + '\\' + 'generate_html' + '\\'
    if dir == 'customersave':
        return os.getcwd() + os.path.sep + 'customer' + '\\' + 'saved_data' + '\\'
    if dir == 'multisave':
        return os.getcwd() + os.path.sep + 'multi' + '\\' + 'saved_data' + '\\'


def different_priority_stock():
    code_list = pd.read_csv('name.csv')['ts_code'].values.tolist()
    today = datetime.datetime.today().strftime('%Y%m%d')
    last_year = datetime.datetime.today() - datetime.timedelta(days=365)
    last_year = last_year.strftime('%Y%m%d')
    for code in code_list:
        priority = 2
        df = setdata(last_year, today, code)
        max_price = max(df['close'].values.tolist())
        min_price = min(df['close'].values.tolist())
        today_close = df['close'].values.tolist()[-1]
        if (today_close > 2 * min_price) or (today_close > 0.8 * max_price):
            priority = 1
        print(code,max_price, min_price, today_close, priority)
        with open('priority.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([code, priority])


mkdir(os.getcwd() + os.path.sep + 'customer')
mkdir(os.getcwd() + os.path.sep + 'saved_data')
create_all_dir()
create_customer_dir()
create_csv()
# save_trade_date()
# find_real_start_end('20220701', 20230119)

# connect_database('23.94.43.9',3306,'root','qwer12345')
# different_priority_stock()
