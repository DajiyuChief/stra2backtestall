import math
import os
# import sys
from collections import namedtuple
from operator import attrgetter

import easyquotation

import gol_all
# from gol import set_value,get_value, _init
import numpy as np
import pandas as pd
import time
# import efinance as ef
# import pymysql
import tushare as ts
import talib as ta
import datetime
from datetime import date, datetime, timedelta
from chinese_calendar import is_holiday
import csv

from baseFun import find_real_start_end, pull_stock_name, pull_fun_name

pro = ts.pro_api('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
# 设置数据接口
quotation = easyquotation.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
quotation_daykline = easyquotation.use('daykline')

# sys.path.append("../data_modules/database_connection.py")
# 初始化全局变量
gol_all._init()
#
# 回测前一交易日数据
yesterday_data = pd.DataFrame
# 回测当前交易数据
now_data = pd.DataFrame
# 第二天数据
second_data = pd.DataFrame
# 第三天数据
third_data = pd.DataFrame
# 当前历史数据
history_data = pd.DataFrame
# 至少240日历史数据
history_240 = pd.DataFrame
# 全局数据
global_data = pd.DataFrame
# 对应买卖条件中第三条变化的RSI
variety_rsi = 0.1
# 记录条件三的日期
history_condition = pd.DataFrame
# 开始日期
gol_start = ''
# 结束日期
gol_end = ''
# 股票代码
stock_code = ''
# 条件三条件标志
condition_flag = 1
# 记录条件三执行几次
condition_step = 0
# 记录买卖信号
# 仓位，单位是股数
num = 0
# 记录buy sell 中的cost
cost = 0
# 数据库
# db = database_connection.MySQLDb()
# 总资产
all = 0
# 资金
principal = 0
# 起始资金数，用于判断是否需要强制止损
begin = 0
# 记录交易开放时间
transaction_date = []
# 记录交易时间表
# 买卖日期
buy_signal = []
sell_signal = []
# 记录中线条件的交易日期
middle_date = []
# 中线条件的买卖日期
middle_buy_list = []
middle_sell_list = []
# 记录中线条件其实日期
middle_start_date = ''
# 中线是否可执行标志位
# 记录当前中线条件的所属日期
middle_time = ''
# 记录上次中线条件下买卖的时间
middle_last_date = ''
# 定义结构体储存数据
# 分别是当前时间，优先级，类型（买卖），所属时间（穿中线用）
MyStruct = namedtuple("MyStruct", "date priority type time")
# 显示所有行
pd.set_option('display.max_rows', 1000)
# 显示所有列
pd.set_option('display.max_columns', 1000)
# 区分回测还是实时
trans_type = ''
# 保存买卖信息，保存到csv中
gol_buy_sell = []


def set_info(start, end, stock, type):
    global stock_code
    global global_data
    global transaction_date
    global buy_signal, sell_signal
    stock_code = stock
    global_data = setdata(start, end, stock)
    clear()
    if type == 'realtime' or type == 'back2all':
        insert_nowdata(stock)
    # boll线
    global_data['upper'], global_data['middle'], global_data['lower'] = ta.BBANDS(
        global_data.close.values,
        timeperiod=20,
        nbdevup=2,
        nbdevdn=2,
        matype=0)
    global_data['upper'] = round(global_data['upper'], 2)
    global_data['middle'] = round(global_data['middle'], 2)
    global_data['lower'] = round(global_data['lower'], 2)
    global_data['rsi'] = ta.RSI(global_data.close.values, timeperiod=6)
    global_data['rsi'] = round(global_data['rsi'], 4)
    global_data['rsi_var'] = global_data['rsi'].diff() / np.roll(global_data['rsi'], shift=1)
    global_data['rsi_var'] = round(global_data['rsi_var'], 4)
    global_data['low-lowboll'] = global_data['low'] - global_data['lower']
    global_data['high-highboll'] = global_data['high'] - global_data['upper']
    global_data['high-mid'] = global_data['high'] - global_data['middle']
    global_data['mid-low'] = global_data['middle'] - global_data['low']
    global_data['close-open'] = global_data['close'] - global_data['open']
    global_data['yes_close-mid'] = global_data['pre_close'] - global_data['middle']
    global_data['mid-close'] = global_data['middle'] - global_data['close']
    global_data['ma5'] = round(global_data['close'].rolling(5).mean(), 2)
    global_data['ma10'] = round(global_data['close'].rolling(10).mean(), 2)
    global_data['ma20'] = round(global_data['close'].rolling(20).mean(), 2)
    global_data['ma30'] = round(global_data['close'].rolling(30).mean(), 2)
    gol_all.set_value(stock_code + 'global_data', global_data)
    transaction_date = global_data['trade_date'].values.tolist()
    return global_data


def clear():
    global transaction_date, buy_signal, sell_signal, middle_date, middle_buy_list, middle_sell_list, middle_start_date, middle_time, middle_last_date, condition_flag
    buy_signal = []
    sell_signal = []
    middle_date = []
    # 中线条件的买卖日期
    middle_buy_list = []
    middle_sell_list = []
    # 所有上穿，下穿中线时间
    middle_start_date = ''
    # 中线是否可执行标志位
    # 记录当前中线条件的所属日期
    middle_time = ''
    # 记录上次中线条件下买卖的时间
    middle_last_date = ''
    transaction_date = []
    condition_flag = 1


def setdata(start_day, end_day, stock_code):
    uncatchable_list = []
    try:
        df = pro.daily(ts_code=stock_code, start_date=start_day, end_date=end_day)
        if len(df) == 0:
            df = pro.fund_daily(ts_code=stock_code, start_date=start_day, end_date=end_day)
    except:
        df = []
        uncatchable_list.append(stock_code)
    df = df.sort_values(by='trade_date', ascending=True)
    return df


# 获取今日数据,插入全局数据
def insert_nowdata(stockcode):
    global global_data
    try:
        df_now = quotation.real(stock_code_convert(stockcode))
        # print(df_now)
    except:
        return
    df_now_dic = list(df_now.values())
    today_split = df_now_dic[0]['date'].split('-')
    today = today_split[0] + today_split[1] + today_split[2]
    glo_date = global_data['trade_date'].values.tolist()
    if today not in glo_date:
        ts_code = stockcode
        trade_date = today
        open = float(df_now_dic[0]['open'])
        high = float(df_now_dic[0]['high'])
        low = float(df_now_dic[0]['low'])
        close = float(df_now_dic[0]['now'])
        pre_close = float(df_now_dic[0]['close'])
        change = close - pre_close
        pct_chg = round(change * 100 / pre_close, 4)
        vol = float(df_now_dic[0]['turnover']) / 100
        amount = float(df_now_dic[0]['volume']) / 1000
        today_info = {'ts_code': ts_code, 'trade_date': trade_date, 'open': open, 'high': high, 'low': low,
                      'close': close, 'pre_close': pre_close, 'change': change, 'pct_chg': pct_chg, 'vol': vol,
                      'amount': amount}
        # print(today_info)
        global_data = global_data.append(today_info, ignore_index=True)


def get_transdate(stockcode, start, end):
    df = setdata(start, end, stockcode)
    df_now = quotation.real(stock_code_convert(stockcode))
    transdate = df['trade_date'].values.tolist()
    df_now_dic = list(df_now.values())
    today_split = df_now_dic[0]['date'].split('-')
    today = today_split[0] + today_split[1] + today_split[2]
    if today not in transdate:
        transdate.append(today)
    return transdate


# 股票代码格式转换
def stock_code_convert(stock_code):
    lst = stock_code.split('.')
    type = lst[1].lower()
    return type + lst[0]


# 计算两个日期之间的交易日
def workdays(start, end):
    # 字符串格式日期的处理
    if type(start) == str:
        start = datetime.strptime(start, '%Y-%m-%d').date()
    if type(end) == str:
        end = datetime.strptime(end, '%Y-%m-%d').date()
    # 开始日期大，颠倒开始日期和结束日期
    if start > end:
        start, end = end, start

    counts = 0
    while True:
        if start > end:
            break
        if is_holiday(start) or start.weekday() == 5 or start.weekday() == 6:
            start += timedelta(days=1)
            continue
        counts += 1
        start += timedelta(days=1)
    return counts


# 日期前推 后推
def date_calculate(date, days):
    try:
        start = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
        day = date
        if days > 0:
            if date >= transaction_date[-days]:
                return None
            while days > 0:
                start += timedelta(days=1)
                day = start.strftime('%Y%m%d')
                if day in transaction_date:
                    days = days - 1
        elif days < 0:
            if date <= transaction_date[-days - 1]:
                return None
            while days < 0:
                start -= timedelta(days=1)
                day = start.strftime('%Y%m%d')
                if day in transaction_date:
                    days = days + 1
        return day
    except:
        return None


# 返回交易时间列表
def used_date(start, end, stockcode):
    trade_date = find_real_start_end(start, end)
    return trade_date


# 比较三天之内每前后两天的RSI
def compare_RSI(day1, day2, day3, baseline, flag):
    rsi_day1 = getRSI(day1)
    rsi_day2 = getRSI(day2)
    rsi_day3 = getRSI(day3)
    if flag == 1:
        if rsi_day2 > (1 + baseline) * rsi_day1 or rsi_day3 > (1 + baseline) * rsi_day2:
            return True
        else:
            return False
    elif flag == -1:
        if rsi_day2 > (1 - baseline) * rsi_day1 or rsi_day3 > (1 - baseline) * rsi_day2:
            return True
        else:
            return False


def sell_compare_RSI(day1, day2, day3, baseline):
    rsi_day1 = getRSI(day1)
    rsi_day2 = getRSI(day2)
    rsi_day3 = getRSI(day3)
    if rsi_day2 > (1 + baseline) * rsi_day1 or rsi_day3 > (1 + baseline) * rsi_day2:
        return True
    else:
        return False


def winning_percentage():
    data = history_240['close']
    # 5日均线
    five = data.ewm(span=5, adjust=False, min_periods=5).mean().loc[0]
    five_before = data.ewm(span=5, adjust=False, min_periods=5).mean().loc[1]
    # 10日均线
    ten = data.ewm(span=10, adjust=False, min_periods=10).mean().loc[0]
    ten_before = data.ewm(span=10, adjust=False, min_periods=10).mean().loc[1]
    # 20日均线
    twenty = data.ewm(span=20, adjust=False, min_periods=20).mean().loc[0]
    twenty_before = data.ewm(span=20, adjust=False, min_periods=20).mean().loc[1]
    # 40日均线
    forty = data.ewm(span=40, adjust=False, min_periods=40).mean().loc[0]
    forty_before = data.ewm(span=40, adjust=False, min_periods=40).mean().loc[1]
    # 60日均线
    sixty = data.ewm(span=60, adjust=False, min_periods=60).mean().loc[0]
    sixty_before = data.ewm(span=60, adjust=False, min_periods=60).mean().loc[1]
    # 120日均线
    one_hundred_and_twenty = data.ewm(span=120, adjust=False, min_periods=120).mean().loc[0]
    one_hundred_and_twenty_before = data.ewm(span=120, adjust=False, min_periods=120).mean().loc[1]
    # 240日均线
    two_hundred_and_forty = data.ewm(span=240, adjust=False, min_periods=240).mean().loc[0]
    cnt = 0
    if five > ten and five - five_before > 0:
        cnt += 1
    if ten > twenty and five - five_before > 0 and ten - ten_before > 0:
        cnt += 1
    if twenty > forty and five - five_before > 0 and ten - ten_before > 0 and twenty - twenty_before > 0:
        cnt += 1
    if forty > sixty and five - five_before > 0 and ten - ten_before > 0 and twenty - twenty_before > 0 and forty - forty_before > 0:
        cnt += 1
    if sixty > one_hundred_and_twenty and five - five_before > 0 and ten - ten_before > 0 and twenty - twenty_before > 0 and forty - forty_before > 0 and sixty - sixty_before > 0:
        cnt += 1
    if two_hundred_and_forty > one_hundred_and_twenty and five - five_before > 0 and ten - ten_before > 0 and twenty - twenty_before > 0 and forty - forty_before > 0 and sixty - sixty_before > 0 and one_hundred_and_twenty - one_hundred_and_twenty_before > 0:
        cnt += 1
    # 每满足一项条件胜率就增5%
    return cnt * 0.05


def set_cost(date, principal, isWhole):
    price = get_price(date, 'close')
    cost = int(principal / (price * 100))
    if not isWhole:
        # 加仓2p-1
        cost = ((0.7 + winning_percentage()) * 2 - 1) * cost
        # 取满100股
        cost = math.floor(cost / 100) * 100
    return cost


def get_price(date, type):
    if type == 'close':
        return global_data.loc[global_data['trade_date'] == date].close.values[0]
    elif type == 'open':
        return global_data.loc[global_data['trade_date'] == date].open.values[0]
    elif type == 'high':
        return global_data.loc[global_data['trade_date'] == date].high.values[0]
    elif type == 'low':
        return global_data.loc[global_data['trade_date'] == date].low.values[0]


# 改写getBoll()
def getBoll(date):
    global global_data
    high = global_data.loc[global_data['trade_date'] == date].upper.values[0]
    middle = global_data.loc[global_data['trade_date'] == date].middle.values[0]
    low = global_data.loc[global_data['trade_date'] == date].lower.values[0]
    return high, middle, low


# 改写getRSI()
def getRSI(date):
    global global_data
    # # 6日rsi
    rsi = global_data.loc[global_data['trade_date'] == date].rsi.values[0]
    return rsi


def RSI_vary(date):
    todayRSI = getRSI(date)
    yesRSI = getRSI(date_calculate(date, -1))
    var = (todayRSI - yesRSI) / yesRSI
    return var


# 检测特殊情况中有无触高、低线情况
def check_span_days(start, end, type):
    # 从第二天开始比较
    start = date_calculate(start, 1)
    if type == 'buy':
        while start < end:
            high = get_price(start, 'high')
            highBoll = getBoll(start)[0]
            if high >= highBoll:
                return False
            start = date_calculate(start, 1)
        return True
    if type == 'sell':
        while start < end:
            low = get_price(start, 'high')
            lowBoll = getBoll(start)[2]
            if low <= lowBoll:
                return False
            start = date_calculate(start, 1)
        return True


# 检查中线条件
def check_middle(last_date, date):
    # print(last_date,date,transaction_date[-1],datetime.now())
    global variety_rsi
    global condition_flag
    global condition_step
    global middle_date, middle_buy_list, middle_sell_list, middle_start_date, middle_last_date
    # 防止最后三天取不到
    if date is None:
        # print('sss')
        return
    flag = []
    nextday_index = -1
    day2 = date_calculate(date, 1)
    day3 = date_calculate(day2, 1)
    day4 = date_calculate(day3, 1)
    flag.append(buy_check_middle(last_date, date) or sell_check_middle(last_date, date))
    if flag[0] is True:
        # 第一次不看rsi变化率
        if condition_flag == 1:
            middle_last_date = date
            middle_start_date = date
            if buy_check_middle(last_date, date):
                buy_signal.append(MyStruct(date, 2, 'buy', middle_start_date))
                middle_buy_list.append(MyStruct(date, 2, 'buy', middle_start_date))
            else:
                sell_signal.append(MyStruct(date, 2, 'sell', middle_start_date))
                middle_sell_list.append(MyStruct(date, 2, 'sell', middle_start_date))
            # middle_date.append(MyStruct(date,2))
            condition_flag = condition_flag - 1
        else:
            if abs(RSI_vary(date)) > variety_rsi:
                variety_rsi = variety_rsi * 1.5
                middle_last_date = date
                if buy_check_middle(last_date, date):
                    buy_signal.append(MyStruct(date, 2, 'buy', middle_start_date))
                    middle_buy_list.append(MyStruct(date, 2, 'buy', middle_start_date))
                else:
                    sell_signal.append(MyStruct(date, 2, 'sell', middle_start_date))
                    middle_sell_list.append(MyStruct(date, 2, 'sell', middle_start_date))
            else:
                # 穿中线但rsi变化率不满足时
                middle_last_date = last_date
                if buy_check_middle(last_date, date):
                    buy_signal.append(MyStruct(date, 2, 'notbuy', middle_start_date))
                    middle_buy_list.append(MyStruct(date, 2, 'notbuy', middle_start_date))
                else:
                    sell_signal.append(MyStruct(date, 2, 'notsell', middle_start_date))
                    middle_sell_list.append(MyStruct(date, 2, 'notsell', middle_start_date))
                # variety_rsi = variety_rsi * 1.5
        # 记录与上次中线交易日相比，是否满足穿中线的条件
        for day in [day2, day3, day4]:
            if day is None:
                flag.append(False)
            elif date_calculate(middle_last_date, 3) is not None and (day > date_calculate(middle_last_date, 3)):
                flag.append(False)
            elif middle_last_date == last_date:
                flag.append(buy_check_middle(middle_last_date, day) or sell_check_middle(middle_last_date, day))
            else:
                flag.append(buy_check_touch_middle(day) or sell_check_touch_middle(day))
        del (flag[0])
        for i in range(0, 3):
            if flag[i] is True:
                nextday_index = i
                break
        if nextday_index != -1:
            # variety_rsi = variety_rsi * 1.5
            # next_date是除了一次的穿中线的第二天
            next_date = date_calculate(date, nextday_index + 1)
            # print(middle_last_date,next_date,variety_rsi)
            check_middle(middle_last_date, next_date)
        else:
            # print(date)
            # 下穿
            if get_price(date, 'close') < getBoll(date)[1]:
                # 看后三天有没有上穿
                for i in range(1, 4):
                    if date_calculate(date, i) is not None and buy_check_middle(date, date_calculate(date, i)):
                        # fourdays_later四天后，若收盘价高于中线，买入
                        fourdays_later = date_calculate(date, 4)
                        if fourdays_later is None:
                            return
                        if get_price(fourdays_later, 'close') > getBoll(fourdays_later)[1]:
                            buy_signal.append(MyStruct(fourdays_later, 2, 'buy', middle_start_date))
                            middle_buy_list.append(MyStruct(fourdays_later, 2, 'buy', middle_start_date))
                            break
            # 上穿
            elif get_price(date, 'close') > getBoll(date)[1]:
                # 看后三天有没有下穿
                for i in range(1, 4):
                    if date_calculate(date, i) is not None and sell_check_middle(date, date_calculate(date, i)):
                        # fourdays_later四天后，若收盘价仍低于中线卖出
                        fourdays_later = date_calculate(date, 4)
                        if fourdays_later is None:
                            return
                        if get_price(fourdays_later, 'close') < getBoll(fourdays_later)[1]:
                            sell_signal.append(MyStruct(fourdays_later, 2, 'sell', middle_start_date))
                            middle_sell_list.append(MyStruct(fourdays_later, 2, 'sell', middle_start_date))
                            break
            # 初始化条件
            condition_flag = 1
            variety_rsi = 0.1
            middle_date = sorted(middle_buy_list + middle_sell_list, key=attrgetter("date"))
        return middle_buy_list, middle_sell_list, middle_date


# 买入条件：触及下沿线情况
# percent为用户指定的比例
def buy_check_touch_low(percent, end):
    # 股票最低价已经触及布林线下沿线
    flag1 = False
    # 在（1）成立的前提下，出现RSI-6 大于上一日指定比例时买入
    flag2 = False
    lowBoll = getBoll(end)[2]
    low = global_data.loc[global_data['trade_date'] == end].low.values[0]
    i = 0
    if lowBoll >= low:
        flag1 = True
    if flag1:
        while end is not None:
            nowRSI = getRSI(end)
            yesterdayRSI = getRSI(date_calculate(end, -1))
            if nowRSI > (yesterdayRSI * (1 + percent)):
                flag2 = True
                return flag2, i
            end = date_calculate(end, 1)
            i = i + 1
    return flag2, i - 1


# 买入条件：触及中界线情况
def buy_check_touch_middle(end):
    # 股价从下往上越过中界线，即最高价大于中界线
    flag1 = False
    # 收盘为阳线，即收盘价高于开盘价
    flag2 = False
    midBoll = getBoll(end)[1]
    today_close = get_price(end, 'close')
    yes_close = get_price(date_calculate(end, -1), 'close')
    if yes_close < midBoll < today_close:
        flag1 = True
    if flag1:
        open = global_data.loc[global_data['trade_date'] == end].open.values[0]
        close = global_data.loc[global_data['trade_date'] == end].close.values[0]
        if close > open:
            flag2 = True
    return flag2


def buy_check_middle(last_date, date):
    if date is None:
        return None
    # 股价从下往上越过中界线，即最高价大于中界线
    flag1 = False
    # 收盘为阳线，即收盘价高于开盘价
    flag2 = False
    midBoll = getBoll(date)[1]
    today_close = get_price(date, 'close')
    last_date_close = get_price(last_date, 'close')
    if last_date_close < midBoll < today_close:
        flag1 = True
    if flag1:
        open = global_data.loc[global_data['trade_date'] == date].open.values[0]
        close = global_data.loc[global_data['trade_date'] == date].close.values[0]
        if close > open:
            flag2 = True
    return flag2


def buy_check_condition_three(end, rsi_flag=1):
    global variety_rsi
    global condition_flag
    global condition_step
    day2 = date_calculate(end, 1)
    day3 = date_calculate(day2, 1)
    day4 = date_calculate(day3, 1)
    flag_day1 = buy_check_touch_middle(end)
    flag_day2 = check_middle(day2)
    flag_day3 = check_middle(day3)

    if condition_flag == 0:
        if flag_day1 and (flag_day2 or flag_day3) and compare_RSI(end, day2, day3, variety_rsi, rsi_flag):
            variety_rsi = variety_rsi * 1.5
            rsi_flag = rsi_flag * -1
            condition_step = condition_step + 1
            return buy_check_condition_three(day4, rsi_flag)
        condition_flag = 1
        variety_rsi = 0.1
    elif condition_flag == 1:
        if flag_day1:
            condition_flag = 0
            rsi_flag = rsi_flag * -1
            condition_step = condition_step + 1
            return buy_check_condition_three(day2, rsi_flag)
        variety_rsi = 0.1


# 对应文档特殊情况1
def buy_check_special(end):
    # 触及上沿线
    flag1 = False
    flag2 = False
    date = end
    high = global_data.loc[global_data['trade_date'] == end].high.values[0]
    highBoll = getBoll(end)[0]
    if high >= highBoll:
        flag1 = True
    if flag1:
        if date == transaction_date[-1]:
            return
        # 向下循环
        # print(date,transaction_date[-1])
        while date is not None:
            date = date_calculate(date, 1)
            # span_days = workdays(datetime.strptime(end, '%Y%m%d'), datetime.strptime(date, '%Y%m%d'))
            if date is not None:
                span_days = workdays(datetime.strptime(end, '%Y%m%d'), datetime.strptime(date, '%Y%m%d'))
                close = get_price(date, 'close')
                high = get_price(date, 'high')
                # 下降达到中界线
                if close <= getBoll(date)[1]:
                    break
                # 股价下一次触及上沿线
                if (high >= getBoll(date)[0]) & (span_days >= 3):
                    if (getRSI(date) <= 80) & check_span_days(end, date, 'buy'):
                        buy_signal.append(MyStruct(date, 1, 'buy', date))
                        # print('buy 特1触高线', date)
                        flag2 = True
                    break
    return flag2


def buy(stock_code, isCharge, day, isWhole, type):
    global num
    global cost
    global all
    global principal
    global gol_buy_sell

    price = get_price(day, 'close')
    high = get_price(day, 'high')
    cost = set_cost(day, principal, isWhole)
    charge = 0
    if cost > 0:
        num += cost * 100
        principal -= cost * price * 100
        charge = 0
        if isCharge:
            charge = cost * price * 100 * 0.0003
            # 佣金最低5元
            if charge < 5:
                charge = 5
            principal -= charge
            all -= charge
        while principal < 0:
            cost -= 1
            num -= 100
            principal += price * 100
    if num > 0:
        gol_buy_sell.append([stock_code, day, 1, price, high, principal + num * price])
        # print(stock_code, day, 1, price, high)
        # if type == 'backtest':
        #     sql = "INSERT IGNORE INTO backtest2all(CODE, DATE, TYPE, PRICE, NUM, poundage, stoploss, total, HIGH) \
        #                                                 VALUES ('%s', '%s',  %d,  %f,  %f, %f, %d, %f, %f)" % \
        #           (stock_code, day, True, price, num, charge, False, all, high)
        # elif type == 'realtime':
        #     sql = "INSERT IGNORE INTO actual2all(CODE, DATE, TYPE, PRICE, NUM, poundage, stoploss, total, HIGH) \
        #                                                             VALUES ('%s', '%s',  %d,  %f,  %f, %f, %d, %f, %f)" % \
        #           (stock_code, day, True, price, num, charge, False, all, high)
        # db.commit_data(sql)
        # print(day + " " + "buy: " + str(num) + "股 " + "价格：" + str(price) + " 剩余本金： " + str(
        #     principal) + " 总资产： " + str(all) + " 手续费： " + str(charge))


# 卖出条件：触及上沿线情况
# percent为用户指定的比例
def sell_check_touch_high(percent, end):
    # 股票最高价已经触及布林线上沿线
    flag1 = False
    # 在（1）成立的前提下，在出现RSI-6 小于上一日指定比例时卖出
    flag2 = False
    yes = date_calculate(end, -1)
    highBoll = getBoll(end)[0]
    high = global_data.loc[global_data['trade_date'] == end].high.values[0]
    i = 0
    if high >= highBoll:
        flag1 = True
    if flag1:
        while end is not None:
            nowRSI = getRSI(end)
            yesterdayRSI = getRSI(date_calculate(end, -1))
            # print(end,nowRSI,yesterdayRSI)
            if nowRSI < (yesterdayRSI * (1 - percent)):
                flag2 = True
                return flag2, i
            end = date_calculate(end, 1)
            i = i + 1
    return flag2, i - 1


# 卖出条件：触及中界线情况
def sell_check_touch_middle(end):
    # 股价从上往下越过中界线，即最低价小于中界线
    flag1 = False
    # 收盘为阴线，即收盘价低于开盘价
    flag2 = False
    midBoll = getBoll(end)[1]
    today_clsoe = get_price(end, 'close')
    yes_close = get_price(date_calculate(end, -1), 'close')
    if today_clsoe < midBoll < yes_close:
        flag1 = True
    if flag1:
        open = global_data.loc[global_data['trade_date'] == end].open.values[0]
        close = global_data.loc[global_data['trade_date'] == end].close.values[0]
        if close < open:
            flag2 = True
    return flag2


def sell_check_middle(last_date, date):
    # 股价从上往下越过中界线，即最低价小于中界线
    flag1 = False
    # 收盘为阴线，即收盘价低于开盘价
    flag2 = False
    midBoll = getBoll(date)[1]
    today_clsoe = get_price(date, 'close')
    last_date_close = get_price(last_date, 'close')
    if today_clsoe < midBoll < last_date_close:
        flag1 = True
    if flag1:
        open = global_data.loc[global_data['trade_date'] == date].open.values[0]
        close = global_data.loc[global_data['trade_date'] == date].close.values[0]
        if close < open:
            flag2 = True
    return flag2


def sell_check_condition_three(end, rsi_flag=-1):
    global variety_rsi
    global condition_flag
    global condition_step
    # 考虑交易日
    day2 = date_calculate(end, 1)
    day3 = date_calculate(day2, 1)
    day4 = date_calculate(day3, 1)
    flag_day1 = sell_check_touch_middle(end)
    flag_day2 = sell_check_touch_middle(day2)
    flag_day3 = sell_check_touch_middle(day3)

    if condition_flag == 0:
        if flag_day1 and (flag_day2 or flag_day3) and compare_RSI(end, day2, day3, variety_rsi, rsi_flag):
            variety_rsi = variety_rsi * 1.5
            rsi_flag = rsi_flag * -1
            condition_step = condition_step + 1
            return sell_check_condition_three(day4, rsi_flag) * -1
        condition_flag = 1
        variety_rsi = 0.1
        # print('sell',condition_step)
        return 1
    elif condition_flag == 1:
        if flag_day1:
            condition_flag = 0
            rsi_flag = rsi_flag * -1
            # variety_rsi = variety_rsi * 1.5
            condition_step = condition_step + 1
            return sell_check_condition_three(day2, rsi_flag) * -1
        variety_rsi = 0.1
        # print('sell',condition_step)
        return 1


# 对应文档特殊情况2
def sell_check_special(end):
    # 触及下沿线
    flag1 = False
    flag2 = False
    date = end
    low = global_data.loc[global_data['trade_date'] == end].low.values[0]
    lowBoll = getBoll(end)[2]
    if low <= lowBoll:
        flag1 = True
    if flag1:
        # 回溯前30天
        if date == transaction_date[-1]:
            return
        while date is not None:
            date = date_calculate(date, 1)
            # next_date = date_calculate(date, 1)
            if date is not None:
                span_days = workdays(datetime.strptime(end, '%Y%m%d'), datetime.strptime(date, '%Y%m%d'))
                close = get_price(date, 'close')
                low = get_price(date, 'low')
                # 上升达到中界线
                if close >= getBoll(date)[1] or low <= getBoll(date)[2]:
                    break
                # 股价下一次触及下沿线
                if (low <= getBoll(date)[2]) & (span_days >= 3):
                    if check_span_days(end, date, 'sell'):
                        if (getRSI(date) >= 20):
                            sell_signal.append(MyStruct(date, 1, 'sell', date))
                            # print('sell 特2触低线', date)
                            flag2 = True
                            break
                        elif date == transaction_date[-1]:
                            return
                        elif get_price(date_calculate(date, 1), 'low') < getBoll(date_calculate(date, 1))[2]:
                            sell_signal.append(MyStruct(date_calculate(date, 1), 1, 'sell', date_calculate(date, 1)))
                            break
    return flag2


# 特殊情况3 最高价触及了上沿、最低价也触及了下沿
def check_special(end):
    highBoll = getBoll(end)[0]
    high = global_data.loc[global_data['trade_date'] == end].high.values[0]
    lowBoll = getBoll(end)[2]
    low = global_data.loc[global_data['trade_date'] == end].low.values[0]
    rsi = getRSI(end)

    # if rsi > 80:
    #     sell_signal.append(MyStruct(end, 1, 'sell', end))
    #     # print('sell rsi大于80', end)
    #     return -1
    # if rsi < 20:
    #     buy_signal.append(MyStruct(end, 1, 'buy', end))
    #     # print('buy rsi小于20', end)
    #     return 1

    if high >= highBoll and lowBoll >= low:
        open = global_data.loc[global_data['trade_date'] == end].open.values[0]
        close = global_data.loc[global_data['trade_date'] == end].close.values[0]
        # 阴线收盘
        if open > close:
            sell_signal.append(MyStruct(end, 1, 'sell', end))
            # print('sell 阴线收盘', end)
            return -1
        # 阳线收盘
        if open < close:
            buy_signal.append(MyStruct(end, 1, 'buy', end))
            # print('buy 阳线收盘', end)
            return 1
    # 特数情况rsi大于80或rsi小于20
    return 0


def buy_check(percent, end):
    if check_special(end) == 1:
        return True
    if buy_check_special(end):
        return True
    # 如果买入条件1与卖出条件2同时出现，先执行卖出条件2；
    return False


def sell_check(percent, end):
    if check_special(end) == -1:
        return True
    if sell_check_special(end):
        return True
    # 如果买入条件2与卖出条件1同时出现，先执行买入条件2；
    return False


def sell(stock_code, isCharge, day, type):
    global num
    global cost
    global all
    global principal
    global gol_buy_sell
    # if sell_check(percent, day) and num > 0:
    price = get_price(day, 'close')
    high = get_price(day, 'high')
    principal += num * price
    all = principal
    charge = 0
    stamp_tax = 0
    if isCharge:
        charge = cost * price * 100 * 0.0003
        # 佣金最低5元
        if charge < 5:
            charge = 5
        # 印花税
        stamp_tax = cost * price * 100 * 0.001
        charge += stamp_tax
        principal -= charge
        all -= charge

    gol_buy_sell.append([stock_code, day, 0, price, high, principal])
    # print(stock_code, day , 0 , price ,high)
    num = 0


# 止损
def stop_loss(stock_code, isCharge, day, type):
    global num
    global cost
    global all
    global principal
    global begin

    price = get_price(day, 'close')
    high = get_price(day, 'high')
    print("强制止损")
    principal += num * price
    all = principal
    charge = 0
    stamp_tax = 0
    if isCharge:
        charge = cost * price * 100 * 0.0003
        # 佣金最低5元
        if charge < 5:
            charge = 5
        # 印花税
        stamp_tax = cost * price * 100 * 0.001
        charge += stamp_tax
        principal -= charge
        all -= charge
        gol_buy_sell.append([stock_code, day, 0, price, high])
        # print(stock_code, day, 'sell', price, high)




def find_max_price(start_date, end_date):
    # 找到截至日期为止最大的价格，用于止损
    price_list = []
    while start_date < end_date:
        price_list.append(get_price(start_date, 'close'))
        start_date = date_calculate(start_date, 1)
    return max(price_list)


def check_stop(stoploss):
    buy_list = sorted(buy_signal, key=attrgetter("date"))
    buy_date = [item.date for item in buy_list]
    buy_date = sorted(list(set(buy_date)))
    stop_signal = []
    if len(buy_date) == 0:
        return stop_signal
    while len(buy_date) > 1:
        flag = 1
        start = buy_date[0]
        end = buy_date[1]
        # buy_price = get_price(start, 'close')
        test_date = start
        while test_date < end:
            test_date = date_calculate(test_date, 1)
            buy_price = find_max_price(start, test_date)
            now_price = get_price(test_date, 'close')
            if now_price < (1 - stoploss) * buy_price:
                stop_signal.append(MyStruct(test_date, 1, 'stop', buy_date[0]))
                buy_date.pop(0)
                flag = 0
                break
        if flag == 1:
            buy_date.pop(0)
    last_date = buy_date[0]
    if last_date < gol_end and len(buy_date) == 1:
        # buy_price = get_price(last_date, 'close')
        # buy_price = find_max_price(last_date, gol_end)
        test_date2 = last_date
        while test_date2 < gol_end:
            test_date2 = date_calculate(test_date2, 1)
            if test_date2 is None:
                return stop_signal
            buy_price = find_max_price(last_date, test_date2)
            now_price = get_price(test_date2, 'close')
            if now_price < (1 - stoploss) * buy_price:
                stop_signal.append(MyStruct(test_date2, 1, 'stop', buy_date[0]))
                break
    return stop_signal


# 获取对应中线条件日期长度
def get_middle_len(date):
    tran = []
    for item in middle_date:
        if item.time == date and item.priority == 2:
            tran.append(item)
    return len(tran)


# 获取中线条件中日期的位置
def get_middle_position(date, time):
    tran = []
    for item in middle_date:
        if item.time == time and item.priority == 2:
            tran.append(item.date)
    # print(tran,date,time,middle_date)
    return tran.index(date)


def check_isdown(date):
    if date == transaction_date[0]:
        return False
    yes = date_calculate(date, -1)
    yes_ma30 = global_data.loc[global_data['trade_date'] == yes].ma30.values[0]
    today_ma30 = global_data.loc[global_data['trade_date'] == date].ma30.values[0]
    yes_ma20 = global_data.loc[global_data['trade_date'] == yes].ma20.values[0]
    today_ma20 = global_data.loc[global_data['trade_date'] == date].ma20.values[0]
    if (today_ma30 < yes_ma30) and (today_ma20 < yes_ma20) and getRSI(date) >= 20:
        return True
    return False


# 参数从左到右依次是初始本金，股票代码，RSI-6变化比率，止损比率，回测周期，是否计算手续费
def new_trans(stock_code, stoploss, isCharge, isWhole, downnotbuy):
    global can_middle_flag, condition_step, middle_time, middle_date
    # 止损日期
    stop_signal = check_stop(stoploss)
    buy_price_list = []
    max_price = 0
    trans = buy_signal + sell_signal + stop_signal
    # trans = buy_signal + sell_signal
    trans = list(set(trans))
    trans = sorted(trans, key=attrgetter("date"))
    middle_date = [item for item in trans if item.priority == 2]
    # print(trans)
    if len(trans) == 0:
        return
    # check_stop(stoploss)
    # print('buy', buy_signal)
    # print('sell', sell_signal)
    # 记录是否有中线条件执行
    is_middle_processing = 0
    # 记录当前交易类型
    trans_flag = 'buy'
    # 上一次买日期，判断止损
    last_buy_date = trans[0].date
    # 已经交易过的中线日期
    already_trans_middle_date = []
    while len(trans) != 0:
        item = trans[0]
        if len(trans) > 1 and trans[0].date == trans[1].date:
            if trans[0].type != trans[1].type:
                trans.pop(1)
        # if last_trans_date == trans[0].date:
        #     trans.pop(0)
        if trans_flag == 'buy':
            # for item in trans:
            # if len(buy_price_list) != 0:
            #     max_price = max(buy_price_list)
            if 'buy' not in item.type:
                trans.pop(0)
                continue
            if downnotbuy:
                if check_isdown(item.date):
                    trans.pop(0)
                    continue
            if item.priority == 1:
                # print('buy1')
                buy(stock_code, isCharge, item.date, isWhole, trans_type)
                trans.pop(0)
                trans_flag = 'sell'
                last_buy_date = item.date
                condition_step = 0
            elif item.priority == 2:
                if condition_step == 0:
                    # 从第一个穿中线就买
                    if item.time == item.date:
                        # print('buy2')
                        # print(2, item.time, item.date)
                        # print(item)
                        middle_time = item.time
                        buy(stock_code, isCharge, item.date, isWhole, trans_type)
                        trans.pop(0)
                        trans_flag = 'sell'
                        last_buy_date = item.date
                        condition_step = condition_step + 1
                    # item.time != item.date 中途开始买情况
                    elif date_calculate(item.time, 3) is not None and date_calculate(item.time, 3) > item.date:
                        # print(2, item.time, item.date)
                        # print(item in middle_date)
                        # print('buy2')
                        middle_time = item.time
                        buy(stock_code, isCharge, item.date, isWhole, trans_type)
                        trans.pop(0)
                        trans_flag = 'sell'
                        last_buy_date = item.date
                        condition_step = get_middle_position(item.date, item.time) + 1
                    else:
                        # print(item,1)
                        trans.pop(0)
                        continue
                elif item.type == 'notbuy' and item.time == middle_time:
                    # print(item, 2)
                    trans.pop(0)
                    condition_step = condition_step + 1
                elif condition_step < get_middle_len(middle_time) and item.time == middle_time:
                    # print(item.time, item.date,middle_time)
                    # print('buy2')
                    buy(stock_code, isCharge, item.date, isWhole, trans_type)
                    trans.pop(0)
                    trans_flag = 'sell'
                    last_buy_date = item.date
                    # condition_step = condition_step + 1
                    condition_step = get_middle_position(item.date, item.time) + 2
                else:
                    # print(condition_step,item, get_middle_len(middle_time),middle_time)
                    trans.pop(0)
                if condition_step == get_middle_len(middle_time):
                    condition_step = 0
            elif item.priority == 3:
                # print('buy3')
                buy(stock_code, isCharge, item.date, isWhole, trans_type)
                trans.pop(0)
                trans_flag = 'sell'
                last_buy_date = item.date
                condition_step = 0
        elif trans_flag == 'sell':
            # for item in trans:
            if 'sell' not in item.type and 'stop' not in item.type:
                trans.pop(0)
                continue
            if item.type == 'stop':
                if item.time == last_buy_date:
                    stop_loss(stock_code, isCharge, item.date, trans_type)
                    trans.pop(0)
                    trans_flag = 'buy'
                    condition_step = 0
                    continue
            if item.priority == 1:
                # print(1, item.time, item.date)
                # print('sell1')
                sell(stock_code, isCharge, item.date, trans_type)
                trans.pop(0)
                trans_flag = 'buy'
                condition_step = 0
            elif item.priority == 2:
                if condition_step == 0:
                    if item.time == item.date:
                        # print(2,item.time, item.date)
                        # print('sell2')
                        middle_time = item.time
                        sell(stock_code, isCharge, item.date, trans_type)
                        trans.pop(0)
                        trans_flag = 'buy'
                        condition_step = condition_step + 1
                    elif date_calculate(item.time, 3) is not None and date_calculate(item.time, 3) > item.date:
                        # print(2, item.time, item.date)
                        # print('sell2')
                        middle_time = item.time
                        sell(stock_code, isCharge, item.date, trans_type)
                        trans.pop(0)
                        trans_flag = 'buy'
                        last_buy_date = item.date
                        condition_step = get_middle_position(item.date, item.time) + 1
                    else:
                        trans.pop(0)
                        continue
                elif item.type == 'notsell' and item.time == middle_time:
                    trans.pop(0)
                    condition_step = condition_step + 1
                elif condition_step < get_middle_len(middle_time) and item.time == middle_time:
                    # print(2,item.time, item.date)
                    # print('sell2')
                    sell(stock_code, isCharge, item.date, trans_type)
                    trans.pop(0)
                    trans_flag = 'buy'
                    condition_step = condition_step + 1
                else:
                    trans.pop(0)
                if condition_step == get_middle_len(middle_time):
                    condition_step = 0
            elif item.priority == 3:
                # print('sell3')
                sell(stock_code, isCharge, item.date, trans_type)
                trans.pop(0)
                trans_flag = 'buy'
                condition_step = 0


def trading_strategy2_position(principa, stock_code, percent, stoploss, span, isCharge, isWhole, transdate, downnotbuy):
    global history_240
    global condition_step
    global num
    global cost
    global all
    global principal
    global begin
    global buy_signal, sell_signal
    # 回测日期列表
    day = transdate
    # 仓位，单位是股数
    num = 0
    # 总资产数
    principal = principa
    all = principal
    # 起始资金数，用于判断是否需要强制止损
    begin = principal
    # 用迭代器跳过指定天数
    day_iter = iter(day)
    for d in day_iter:
        yesterday = date_calculate(d, -1)
        price = get_price(d, 'close')
        # 单笔交易至少有100股
        if True:
            buy_check(percent, d)
            if buy_check_touch_low(percent, d)[0]:
                span_days = buy_check_touch_low(percent, d)[1]
                new_day = date_calculate(d, span_days)
                price = get_price(new_day, 'close')
                # print('buy 触低线', new_day)
                if not isWhole:
                    sell_check_condition_three(d)
                    if condition_step == 0:
                        buy_signal.append(MyStruct(new_day, 3, 'buy', new_day))
                else:
                    buy_signal.append(MyStruct(new_day, 3, 'buy', new_day))
        # 确保有可卖出的股数
        if True:
            sell_check(percent, d)
            if sell_check_touch_high(percent, d)[0]:
                span_days = sell_check_touch_high(percent, d)[1]
                new_day = date_calculate(d, span_days)
                price = get_price(new_day, 'close')
                # print('sell 触高线', new_day)
                if not isWhole:
                    buy_check_condition_three(d)
                    if condition_step == 0:
                        sell_signal.append(MyStruct(new_day, 3, 'sell', new_day))
                else:
                    sell_signal.append(MyStruct(new_day, 3, 'sell', new_day))
            check_middle(yesterday, d)
        # 强制止损
        # if num != 0 and all < begin and abs(all - principal - begin) >= stoploss * (all - principal):
        #     stop_loss(stock_code, isCharge, d, trans_type)
    # transaction(stock_code, stoploss, isCharge, isWhole)
    new_trans(stock_code, stoploss, isCharge, isWhole, downnotbuy)

    # print("共计： " + str(span) + "个交易日")
    # print('---------------------------------------------------------------------------------------------------------')
    print('---------------------------------------------------------------------------------------------------------')
    return all


def date_backtest2(start_day, end_day, stock_code, principal, percent, stoploss, isCharge, isWhole):
    global gol_start, gol_end, trans_type
    trans_type = 'backtest'
    start = datetime(int(start_day[0:4]), int(start_day[4:6]), int(start_day[6:8]))
    end = datetime(int(end_day[0:4]), int(end_day[4:6]), int(end_day[6:8]))
    startbak = start_day
    endbak = end_day
    span = workdays(start, end)
    day = end
    delta = timedelta(days=240 * 1.5 + 100)  # 采取时间差*1.5+100的方式确保能获得足够的交易日
    n_days_forward = day - delta  # 当前日期向前推n天的时间
    day = day + timedelta(days=15)
    start_day = n_days_forward.strftime('%Y%m%d')
    end_day = day.strftime('%Y%m%d')
    # 往后推半个月 确保能取满周期
    set_info(start_day, end_day, stock_code, 'backtest')
    transdate = used_date(startbak, endbak, stock_code)
    gol_start = startbak
    gol_end = endbak
    print(start, end, span, day, delta, n_days_forward, start_day, end_day, stock_code)
    # db.clean_table("TRUNCATE TABLE `backtest2`;")
    return trading_strategy2_position(principal, stock_code, percent, stoploss, span, isCharge, isWhole, transdate)


def realtime(stock_code, principal, percent, stoploss, isCharge, isWhole, days):
    global gol_end, trans_type
    trans_type = 'realtime'
    end = date.today()
    offset1 = timedelta(days=-(days * 3 + 100))
    start = end + offset1
    end_ymd = end.strftime('%Y%m%d')
    gol_end = end_ymd
    start_ymd = (end + offset1).strftime('%Y%m%d')
    # 第二次设置长时间，保证取到所有需要的值
    set_info(start_ymd, end_ymd, stock_code, 'realtime')
    transdate = global_data['trade_date'][-days:].values.tolist()
    print(transdate[0], transdate[-1], stock_code)
    return trading_strategy2_position(principal, stock_code, percent, stoploss, days, isCharge, isWhole, transdate)


def backtest2_all(start_day, end_day, condition_rsi, stoploss):
    df = pd.concat([pull_stock_name(), pull_fun_name()], ignore_index=True)
    code_list = df['ts_code'].values.tolist()


def run2_all(code_list, start_day, end_day, condition_rsi, stoploss, principal, downnotbuy, winpercent, customer_flag):
    global trans_type, gol_buy_sell
    trans_type = 'backtest'
    start = datetime(int(start_day[0:4]), int(start_day[4:6]), int(start_day[6:8]))
    offset = timedelta(days=150)
    start = start - offset
    start_ymd = start.strftime('%Y%m%d')
    today = date.today().strftime('%Y%m%d')
    if end_day == today:
        trans_type = 'back2all'
    time1 = datetime.now()
    for code in code_list:
        try:
            print('正在回测' + code, trans_type, start_ymd, end_day)
            set_info(start_ymd, today, code, trans_type)
            transdate = used_date(start_day, end_day, code)
            trading_strategy2_position(principal, code, condition_rsi, stoploss, 0, False, True, transdate, downnotbuy)
            save_back_tocsv(code, start_day, end_day, condition_rsi, stoploss, downnotbuy, winpercent, customer_flag)
            time.sleep(1)
        except Exception as e:
            print(e)
            continue


# 回测数据写入csv，防止数据库不稳定
def save_back_tocsv(code, start, end, rsi, stoploss, downnotbuy, winpercent, customer_flag):
    global gol_buy_sell
    start_principal = gol_buy_sell[0][-1]
    end_principal = gol_buy_sell[-1][-1]
    if not customer_flag:
        csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(downnotbuy) + '\\' + start + end + str(
            rsi).replace('.', '') + str(
            stoploss).replace('.', '') + str(
            downnotbuy) + '.csv'
        if end_principal >= (1 + winpercent) * start_principal:
            global_data.to_csv(
                os.getcwd() + os.path.sep + 'multi' + '\\' + 'saved_data' + '\\' + str(code).replace('.', '') + '.csv')
    elif customer_flag:
        csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
            downnotbuy) + '\\' + start + end + str(rsi).replace('.',
                                                                '') + str(
            stoploss).replace('.', '') + str(
            downnotbuy) + '.csv'
        global_data.to_csv(
            os.getcwd() + os.path.sep + 'customer' + '\\' + 'saved_data' + '\\' + str(code).replace('.', '') + '.csv')

    with open(csv_path, 'a',
              encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(gol_buy_sell)
        gol_buy_sell = []

# date_backtest2('20220325', '20220614', '600073.SH', 9999999, 0.1, 0.3, False, True)
# save_back_tocsv()
# df = pd.read_csv('back_all.csv').drop_duplicates()
# print(df)

# 调用示例：
# backtest2(30, '300917.SZ', 9999999, 0.1, 0.1, False, True)
# date_backtest2('20220701', '20230119', '300218.SZ', 100000, 0.1, 0.2, False, True)
