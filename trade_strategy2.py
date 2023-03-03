# -*- coding: utf-8 -*-
# @Time : 2023/2/5 9:23
# @Author : Dajiyu
# @File : trade_strategy2.py

import math
import os
import traceback
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

from baseFun import find_real_start_end, get_path, write_to_csv, mkdir, create_finished_list,get_name

pro = ts.pro_api('f558cbc6b24ed78c2104e209a8a8986b33ec66b7c55bcfa2f46bc108')
quotation = easyquotation.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
# 显示所有行
pd.set_option('display.max_rows', 1000)
# 显示所有列
pd.set_option('display.max_columns', 1000)

# 每日记录
trade_record = []
transaction_date = []
calculate_list = []

# trade_flag_list = pd.DataFrame
trade_flag_list = pd.DataFrame(
    columns=['code', 'date', 'close', 'high', 'low', 'max_price', 'rsi', 'rsi_var', 'trade_type', 'now_buy_sell',
             'pre_middle_date',
             'mid_step', 'common_buy_boll_days', 'common_sell_boll_days', 'sp_boll_days', 'principal', 'stock_num',
             'add_flag', 'add_principal', 'delay_buy', 'low_rsi', 'win_stop'])


# print(code, date, close, high, low, max, rsi, rsi_var, trade_type, now_buy_sell, pre_middle_date, mid_step,
#       common_buy_boll_days, common_sell_boll_days, sp_boll_days, principal, stock_num, add_flag, add_principal,
#       delay_buy)

def set_info(start, end, stock, type):
    """
    设置回测数据
    :param start: 开始时间
    :param end: 结束时间
    :param stock: 股票代码
    :param type: 为realtime，back2all时添加今日数据到data中
    :return:dataframe
    """
    global stock_code
    global global_data
    global calculate_list
    stock_code = stock
    # start = datetime(int(start[0:4]), int(start[4:6]), int(start[6:8]))
    offset = timedelta(days=200)
    # start = start - offset
    # start_ymd = start.strftime('%Y%m%d')
    today = datetime.today().strftime('%Y%m%d')
    start_ymd = (datetime.today() - offset).strftime('%Y%m%d')
    global_data = setdata(start_ymd, today, stock)
    clear()
    if type == 'realtime' or type == 'back2all':
        global_data = insert_nowdata(global_data, stock)
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
    calculate_list = global_data['trade_date'].values.tolist()
    return global_data


def clear():
    """
    清除全局标志位
    :return:
    """
    global transaction_date, buy_signal, sell_signal, middle_date, middle_buy_list, middle_sell_list, middle_start_date, middle_time, middle_last_date, condition_flag, trade_flag_list
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
    # trade_flag_list.drop(trade_flag_list.index,inplace=True)


def setdata(start_day, end_day, stock_code):
    """
    从tushare中获取数据
    :param start_day: 开始日期
    :param end_day: 结束日期
    :param stock_code: 股票代码
    :return: dataframe
    """
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
def insert_nowdata(global_data, stockcode):
    """
    获取今日数据,插入全局数据
    :param global_data: 不包含当日数据的回测数据
    :param stockcode: 股票代码
    :return:
    """
    try:
        df_now = quotation.real(stock_code_convert(stockcode))
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
        global_data = global_data.append(today_info, ignore_index=True)
    return global_data


def stock_code_convert(stock_code):
    """
    将代码从000001.SZ转换为sz000001
    :param stock_code:例如 000001.SZ
    :return:sz000001
    """
    lst = stock_code.split('.')
    type = lst[1].lower()
    return type + lst[0]


def date_calculate(date, days):
    """
    日期前推后推多少个交易日
    :param transaction_date: 交易日列表
    :param date: 当前日期
    :param days: 前推 后推多少交易日 负值前推，正值后推
    :return: 计算后日期
    """
    global calculate_list
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nowtime = time[11:13]
    if nowtime[0] == 0:
        # 把时间截取一下以判断早中晚
        # 如果nowtime前面带有0，比如08，把0去掉
        # 如果nowtime第一位不是0，如20，不作处理
        nowtime = nowtime[1]
    if int(nowtime) < 10:
        date = calculate_list[-1]
    # print(global_data)
    # print(calculate_list)
    try:
        index = calculate_list.index(date)
        if days > 0:
            if date >= calculate_list[-days]:
                return None
            else:
                day = calculate_list[index + days]
        elif days < 0:
            if date <= calculate_list[-days - 1]:
                return None
            else:
                day = calculate_list[index + days]
        return day
    except:
        return None


def used_date(start, end):
    """
    返回开始到结束日期之间的交易日列表
    :param start: 开始时间
    :param end: 结束时间
    :return: 交易日列表
    """
    global transaction_date
    trade_date = find_real_start_end(start, end)
    # transaction_date = trade_date
    return trade_date


def get_price(date, type):
    """
    获取对应日期价格
    :param date: 日期
    :param type: 价格类型
    :return: 获取到的价格
    """
    if type == 'close':
        return global_data.loc[global_data['trade_date'] == date].close.values[0]
    elif type == 'open':
        return global_data.loc[global_data['trade_date'] == date].open.values[0]
    elif type == 'high':
        return global_data.loc[global_data['trade_date'] == date].high.values[0]
    elif type == 'low':
        return global_data.loc[global_data['trade_date'] == date].low.values[0]


def getBoll(date):
    """
    获取boll值
    :param date: 日期
    :return: 由高中低boll值组成的列表
    """
    global global_data
    high = global_data.loc[global_data['trade_date'] == date].upper.values[0]
    middle = global_data.loc[global_data['trade_date'] == date].middle.values[0]
    low = global_data.loc[global_data['trade_date'] == date].lower.values[0]
    return high, middle, low


def getRSI(date):
    """
    获取rsi值
    :param date: 日期
    :return: 对应日期rsi
    """
    global global_data
    # # 6日rsi
    date = str(date)
    rsi = global_data.loc[global_data['trade_date'] == date].rsi.values[0]
    return rsi


def RSI_vary(date):
    """
    获取rsi变化率
    :param date: 日期
    :return: rsi变化率
    """
    date = str(date)
    todayRSI = getRSI(date)
    yesRSI = getRSI(date_calculate(date, -1))
    var = (todayRSI - yesRSI) / yesRSI
    return round(var, 4)


def buy_touch_boll_low(date):
    """
    买入条件:触及下沿线情况
    :param date: 日期
    :return: True or False
    """
    lowBoll = getBoll(date)[2]
    low = global_data.loc[global_data['trade_date'] == date].low.values[0]
    if lowBoll >= low:
        return True
    return False


def sell_touch_boll_high(date):
    """
    买出条件:触及上沿线情况
    :param date:
    :return: True or False
    """
    highBoll = getBoll(date)[0]
    high = global_data.loc[global_data['trade_date'] == date].high.values[0]
    if high >= highBoll:
        return True
    return False


# def buy_touch_middle(date):
#     """
#     检测买入穿中线情况
#     :param date: 日期
#     :return:
#     """
#     high = get_price(date, 'high')
#     close = get_price(date, 'close')
#     open = get_price(date, 'open')
#     midboll = getBoll(date)[1]
#     if (high > midboll) and (close > open):
#         return 1
#     if close < midboll:
#         return 0
#     return -1
#
#
# def sell_touch_middle(date):
#     """
#     检测m,卖出穿中线情况
#     :param date: 日期
#     :return:
#     """
#     low = get_price(date, 'low')
#     close = get_price(date, 'close')
#     open = get_price(date, 'open')
#     midboll = getBoll(date)[1]
#     if (low < midboll) and (open > close):
#         return 1
#     if close > midboll:
#         return 0
#     return -1


def touch_middle(date):
    """
    穿中线情况
    :param date:
    :return: 0 1 -1
    """
    close = get_price(date, 'close')
    midboll = getBoll(date)[1]
    if close <= midboll:
        return 1
    if close > midboll:
        return -1
    return 0


def high_open(date):
    """
    高开
    :param date:
    :return: True or False
    """
    high = get_price(date, 'high')
    close = get_price(date, 'close')
    open = get_price(date, 'open')
    midboll = getBoll(date)[1]
    if (high > midboll) and (close > open):
        return True
    return False


def low_open(date):
    """
    低开
    :param date:
    :return: True or False
    """
    low = get_price(date, 'low')
    close = get_price(date, 'close')
    open = get_price(date, 'open')
    midboll = getBoll(date)[1]
    if (low < midboll) and (open > close):
        return True
    return False


def buy_sp(date):
    """
    特殊条件触及上沿线后又离线，但未达中界线又向上折返再次触及上沿线，此时在再次触及上沿线当日买入,此时如RSI大于80则不买，RSI小于80可买入
    :param date:
    :return: True or False
    """
    high = get_price(date, 'high')
    highboll = getBoll(date)[0]
    if high >= highboll:
        return True
    return False


def sell_sp(date):
    """
    特殊条件触及下沿线后又离线，但未达中界线又向下折返再次触及下沿线，此时在再次触及下沿线当日卖出[ 如果此时手里没有仓位则不操作。]，此时如RSI大于20卖出，待RSI小于20或上穿中线再买；如小于20则保留
    :param date:
    :return: True or False
    """
    low = get_price(date, 'low')
    lowboll = getBoll(date)[2]
    if low <= lowboll:
        return True
    return False


def both_sp(date):
    """
    特殊条件当日股票最高价触及了上沿、最低价也触及了下沿
    :param date:
    :return: 1 0 -1
    """
    high = get_price(date, 'high')
    low = get_price(date, 'low')
    highboll = getBoll(date)[0]
    lowboll = getBoll(date)[2]
    if (high >= highboll) and (low <= lowboll):
        open = get_price(date, 'open')
        close = get_price(date, 'close')
        if close > open:
            return 1
        if open > close:
            return -1
    return 0


def check_isdown(date, downnotbuy):
    """
    检测MA下行情况
    :param date:
    :return: True or False
    """
    # global transaction_date
    # if date == transaction_date[0]:
    #     return False
    yes = date_calculate(date, -1)
    # print(date,yes)
    yes_ma30 = global_data.loc[global_data['trade_date'] == yes].ma30.values[0]
    today_ma30 = global_data.loc[global_data['trade_date'] == date].ma30.values[0]
    yes_ma20 = global_data.loc[global_data['trade_date'] == yes].ma20.values[0]
    today_ma20 = global_data.loc[global_data['trade_date'] == date].ma20.values[0]
    if (today_ma30 < yes_ma30) and (today_ma20 < yes_ma20) and (getRSI(date) >= 20) and downnotbuy:
        return True
    return False


def rsi_low(date):
    """
    RSi低于10、5时加仓
    :param date:
    :return: 0 1 2
    """
    rsi = getRSI(date)
    if rsi < 10:
        return 1
    elif rsi < 5:
        return 2
    else:
        return 0


def stop_win(date):
    """
    止盈 暂不区分高低位股
    :param date:
    :return: True or False
    """
    rsi = getRSI(date)
    if rsi > 90:
        return True
    return False


def high_to_low(pre_middle_date, date):
    """

    :param pre_middle_date:
    :param date:
    :return:
    """
    # pre_close = get_price(pre_middle_date, 'close')
    # today_close = get_price(date, 'close')
    pre_low = get_price(pre_middle_date, 'low')
    today_low = get_price(date, 'low')
    pre_mid = touch_middle(pre_middle_date)
    today_mid = touch_middle(date)
    if low_open(date) or (both_sp(date) == -1):
        return True
    if (pre_mid == 1) and (pre_mid != today_mid) and (pre_low > today_low):
        return True
    return False


def low_to_high(pre_middle_date, date):
    """

    :param pre_middle_date:
    :param date:
    :return:
    """
    pre_high = get_price(pre_middle_date, 'high')
    today_high = get_price(date, 'high')
    pre_mid = touch_middle(pre_middle_date)
    today_mid = touch_middle(date)
    if high_open(date) or (both_sp(date) == 1):
        return True
    if (pre_mid == -1) and (pre_mid != today_mid) and (pre_high < today_high):
        return True
    return False


def first_mid(date):
    """

    :param date:
    :return:
    """
    yes = date_calculate(date, -1)
    today_mid = touch_middle(date)
    yes_mid = touch_middle(yes)
    today_high = get_price(date, 'high')
    yes_high = get_price(yes, 'high')
    today_low = get_price(date, 'low')
    yes_low = get_price(yes, 'low')
    if today_mid != yes_mid:
        if (today_mid == 1) and (yes_high < today_high):
            return 1
        elif (today_mid == -1) and (yes_low > today_low):
            return -1
    return 0


def rest_days_common_buy_boll(date, percent):
    """

    :param date:
    :param percent:
    :return:
    """
    can_buy = False
    touch_boll_low = buy_touch_boll_low(date)
    rsi_var = RSI_vary(date)
    common_buy_boll_days = 0
    last_flag = trade_flag_list.tail(1)
    last_boll_days = last_flag['common_buy_boll_days'].values[0]
    if (last_boll_days == 0) and touch_boll_low:
        if rsi_var > percent:
            can_buy = True
        else:
            common_buy_boll_days = 1
    elif last_boll_days > 0:
        if rsi_var > percent:
            can_buy = True
        else:
            common_buy_boll_days = 1
    return can_buy, common_buy_boll_days


def rest_days_common_sell_boll(date, percent):
    """

    :param date:
    :param percent:
    :return:
    """
    can_sell = False
    touch_boll_high = sell_touch_boll_high(date)
    rsi_var = RSI_vary(date)
    common_sell_boll_days = 0
    last_flag = trade_flag_list.tail(1)
    last_boll_days = last_flag['common_sell_boll_days'].values[0]
    if (last_boll_days == 0) and touch_boll_high:
        if rsi_var < -percent:
            can_sell = True
        else:
            common_sell_boll_days = 1
    elif last_boll_days < 0:
        if rsi_var < -percent:
            can_sell = True
        else:
            common_sell_boll_days = 1
    return can_sell, common_sell_boll_days


def rest_days_mid(date):
    """

    :param date:
    :return:
    """
    last_flag = trade_flag_list.tail(1)
    last_middle_step = last_flag['mid_step'].values[0]
    rsi_var = RSI_vary(date)
    mid_step = last_middle_step
    if last_middle_step == 0:
        mid_step = 0
        pre_middle_date = ''
        first_mid_flag = first_mid(date)
        high_open_flag = high_open(date)
        low_open_flag = low_open(date)
        both_sp_flag = both_sp(date)
        if low_open_flag or (both_sp_flag == -1) or (first_mid_flag == -1):
            mid_step = -1
            pre_middle_date = date
        elif high_open_flag or (both_sp_flag == 1) or (first_mid_flag == 1):
            mid_step = 1
            pre_middle_date = date
    else:
        pre_middle_date = last_flag['pre_middle_date'].values[0]
        if date_calculate(pre_middle_date, 4) is not None and date_calculate(pre_middle_date, 4) <= date:
            mid_step = 0
            pre_middle_date = ''
        elif last_middle_step > 0:
            if high_to_low(pre_middle_date, date) and (abs(rsi_var) >= 0.1 * pow(1.5, int(last_middle_step) - 1)):
                mid_step = -(last_middle_step + 1)
                pre_middle_date = date
        elif last_middle_step < 0:
            if low_to_high(pre_middle_date, date) and (abs(rsi_var) >= 0.1 * pow(1.5, int(-1 * last_middle_step) - 1)):
                mid_step = -(last_middle_step - 1)
                pre_middle_date = date
    return mid_step, pre_middle_date


def rest_days_sp_bolls(date):
    """

    :param date:
    :return:
    """
    trans_flag = 0
    rsi = getRSI(date)
    last_flag = trade_flag_list.tail(1)
    last_sp_boll_days = last_flag['sp_boll_days'].values[0]
    sp_buy_bolls_flag = buy_sp(date)
    sp_sell_boll_flag = sell_sp(date)
    sp_boll_days = 0
    close = get_price(date, 'close')
    open = get_price(date, 'open')
    mid_boll = getBoll(date)[1]
    if last_sp_boll_days == 0:
        if sp_buy_bolls_flag:
            sp_boll_days = 1
        if sp_sell_boll_flag:
            sp_boll_days = -1
    elif 0 < last_sp_boll_days < 3 and (close > mid_boll):
        sp_boll_days = last_sp_boll_days + 1
    elif -3 < last_sp_boll_days < 0 and (close < mid_boll):
        sp_boll_days = last_sp_boll_days - 1
    elif last_sp_boll_days >= 3 and (close > mid_boll):
        if sp_buy_bolls_flag:
            if rsi < 80 and (close > open):
                trans_flag = 1
                sp_boll_days = 0
            else:
                sp_boll_days = 1
    elif last_sp_boll_days <= -3 and (close < mid_boll):
        if sp_sell_boll_flag:
            if rsi > 20 and (close < open):
                trans_flag = -1
                sp_boll_days = 0
            else:
                sp_boll_days = -1
    return trans_flag, sp_boll_days


def first_day_insert(code, date, percnet, downnotbuy, principal):
    """

    :param code:
    :param date:
    :param percnet:
    :return:
    """
    global trade_flag_list

    touch_boll_low = buy_touch_boll_low(date)
    touch_boll_high = sell_touch_boll_high(date)
    sp_buy = buy_sp(date)
    sp_sell = sell_sp(date)
    sp_both = both_sp(date)
    open_high = high_open(date)
    open_low = low_open(date)
    # middle = touch_middle(date)
    isdown = check_isdown(date, downnotbuy)
    low_rsi = rsi_low(date)
    win_stop = stop_win(date)
    close = get_price(date, 'close')
    high = get_price(date, 'high')
    low = get_price(date, 'low')
    max_price = close
    rsi = getRSI(date)
    rsi_var = RSI_vary(date)
    trade_type = 0
    now_buy_sell = 1
    pre_middle_date = ''
    common_buy_boll_days = 0
    common_sell_boll_days = 0
    sp_boll_days = 0
    mid_step = 0
    can_buy = False
    can_sell = False
    principal = principal
    stock_num = 0
    add_flag = 0
    add_principal = principal
    delay_buy = False
    if touch_boll_low:
        common_buy_boll_days = 1
    if touch_boll_high:
        common_sell_boll_days = -1
    if open_high or (sp_both == 1):
        can_buy = True
        mid_step = 1
    if open_low or (sp_both == -1):
        can_sell = True
        mid_step = -1
    if sp_buy:
        sp_boll_days = 1
    if sp_sell:
        sp_boll_days = -1
    if mid_step == 0:
        flag = first_mid(date)
        if flag != 0:
            mid_step = 1 * flag
            if flag == 1:
                can_buy = True
            elif flag == -1:
                can_sell = True
    if common_buy_boll_days == 1 and rsi_var > percnet:
        can_buy = True
        trade_type = 1
        common_buy_boll_days = 0
        now_buy_sell = -1
    elif open_low or (sp_both == -1) or (first_mid(date) == -1):
        mid_step = -1
        pre_middle_date = date
    if common_sell_boll_days == -1 and rsi_var < -percnet:
        can_sell = True
        common_sell_boll_days = 0
    elif open_high or (sp_both == 1) or (first_mid(date) == 1):
        can_buy = True
        now_buy_sell = -1
        trade_type = 1
        mid_step = 1
        pre_middle_date = date
    if can_buy:
        if isdown:
            delay_buy = True
        else:
            trade_type = 1
            now_buy_sell = -1
            stock_num = principal // close
            principal = principal - stock_num * close

    flag = [code, date, close, high, low, max_price, rsi, rsi_var, trade_type, now_buy_sell, pre_middle_date, mid_step,
            common_buy_boll_days, common_sell_boll_days, sp_boll_days, principal, stock_num, add_flag, add_principal,
            delay_buy, low_rsi, win_stop]
    trade_flag_list.loc[len(trade_flag_list)] = flag
    # print(trade_flag_list.tail(1))

    # list = [code, date, close, high, low, rsi, rsi_var, trade_type, now_buy_sell, pre_buy_date, pre_sell_date,
    #         buy_boll_days, sell_boll_days, mid_step]
    # flag = list + trade_flag
    # trade_flag_list.loc[len(trade_flag_list)] = flag


def rest_days_insert(code, date, percent, stoploss, downnotbuy, principal):
    global trade_flag_list
    last_flag = trade_flag_list.tail(1)
    isdown = check_isdown(date, downnotbuy)
    low_rsi = rsi_low(date)
    win_stop = stop_win(date)
    close = get_price(date, 'close')
    high = get_price(date, 'high')
    low = get_price(date, 'low')
    max_price = close
    rsi = getRSI(date)
    rsi_var = RSI_vary(date)
    trade_type = 0
    now_buy_sell = last_flag['now_buy_sell'].values[0]
    can_buy = False
    can_sell = False
    principal = last_flag['principal'].values[0]
    stock_num = last_flag['stock_num'].values[0]
    add_flag = last_flag['add_flag'].values[0]
    add_principal = 0
    delay_buy = last_flag['delay_buy'].values[0]

    can_common_boll_buy = rest_days_common_buy_boll(date, percent)[0]
    common_buy_boll_days = rest_days_common_buy_boll(date, percent)[1]
    can_common_boll_sell = rest_days_common_sell_boll(date, percent)[0]
    common_sell_boll_days = rest_days_common_sell_boll(date, percent)[1]
    sp_boll_flag = rest_days_sp_bolls(date)[0]
    sp_boll_days = rest_days_sp_bolls(date)[1]
    mid_step = rest_days_mid(date)[0]
    pre_mid_step = last_flag['mid_step'].values[0]
    pre_middle_date = rest_days_mid(date)[1]

    if now_buy_sell == 1:
        if delay_buy and not (
                (close < (1 - stoploss) * max_price) or stop_win(date) or can_common_boll_sell or (
                sp_boll_flag == -1)) and not isdown:
            max_price = close
            trade_type = 1
            now_buy_sell = -1
            stock_num = principal // close
            principal = principal - stock_num * close
            delay_buy = False
            print(date, '买入')
        if can_common_boll_buy or (mid_step > 0) or (sp_boll_flag == 1):
            can_buy = True
        if can_buy:
            if isdown:
                delay_buy = True
            else:
                max_price = close
                trade_type = 1
                now_buy_sell = -1
                stock_num = principal // close
                principal = principal - stock_num * close
                delay_buy = False
                print(date, '买入')
    elif now_buy_sell == -1:
        max_price = max(close, last_flag['max_price'].values[0])
        if (close < (1 - stoploss) * max_price) or stop_win(date) or can_common_boll_sell or (sp_boll_flag == -1):
            if (close < (1 - stoploss) * max_price):
                trade_type = -3
                print(date, '止损')
            elif stop_win(date):
                trade_type = 3
                print(date, '止盈')
            else:
                trade_type = -1
                print(date, '卖出')
            now_buy_sell = 1
            principal = principal + stock_num * close
            stock_num = 0
        elif stock_num > 0 and 0 < low_rsi != add_flag and add_flag < 3:
            max_price = close
            trade_type = 2
            print(date, '加仓')
            add_flag = add_flag + low_rsi
            add_principal = (stock_num // 4) * close - principal
            if add_principal <= 0:
                principal = principal + add_principal
                add_principal = 0
            else:
                principal = (principal + add_principal) - (stock_num // 4) * close
            stock_num = stock_num + (stock_num // 4)
        elif stock_num > 0 and mid_step > 0 and mid_step != pre_mid_step:
            max_price = close
            trade_type = 2
            add_principal = stock_num * close - principal

            if add_principal <= 0:
                principal = principal + add_principal
                add_principal = 0
            else:
                principal = (principal + add_principal) - stock_num * close
            stock_num = stock_num * 2
            print(date, '加仓')
        elif stock_num > 0 and mid_step < 0 and mid_step != pre_mid_step:
            trade_type = -2
            principal = (stock_num // 2) * close + principal
            stock_num = stock_num // 2
            print(date, '减仓')
    flag = [code, date, close, high, low, max_price, rsi, rsi_var, trade_type, now_buy_sell, pre_middle_date, mid_step,
            common_buy_boll_days, common_sell_boll_days, sp_boll_days, principal, stock_num, add_flag, add_principal,
            delay_buy, low_rsi, win_stop]
    trade_flag_list.loc[len(trade_flag_list)] = flag


def first_run(code, percent, stoploss, downnotbuy, principal):
    today = datetime.today().strftime('%Y%m%d')
    offset = offset = timedelta(days=90)
    start = (datetime.today() - offset).strftime('%Y%m%d')
    set_info(today, today, code, 'realtime')
    trans_date = used_date(start, today)
    first_day = trans_date[0]
    rest_days = trans_date[1:]
    first_day_insert(code, first_day, percent, downnotbuy, principal)
    for date in rest_days:
        rest_days_insert(code, date, percent, stoploss, downnotbuy, principal)
    # trade_flag_list.to_csv('trade_flag.csv', index= False)


def not_first_run(code, percent, stoploss, downnotbuy, principal,customer_flag):
    global trade_flag_list
    if not customer_flag:
        path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(downnotbuy) + '\\' + str(percent) + str(
            stoploss) + '\\' + code + '.csv'
    else:
        path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(downnotbuy) + '\\' + str(percent) + str(
            stoploss) + '\\' + code + '.csv'
    df = pd.read_csv(path, dtype={'pre_middle_date': str}, index_col=False)
    trade_flag_list = df
    # print(path)
    last_date = str(df[df['code'] == code].tail(1)['date'].values[0])
    today = datetime.today().strftime('%Y%m%d')
    if last_date == today:
        last_date = str(df[df['code'] == code].tail(2)['date'].values[0])
        trade_flag_list = trade_flag_list.drop(trade_flag_list.tail(1).index)
    set_info(last_date, today, code, 'realtime')
    trans_date = used_date(last_date, today)[1:]
    print(last_date, today, trans_date)
    if len(trans_date) == 0:
        return
    for date in trans_date:
        rest_days_insert(code, str(date), percent, stoploss, downnotbuy, principal)
    # trade_flag_list.to_csv('trade_flag.csv', index=False)


def run(code_list, percent, stoploss, downnotbuy, principal, winpercent, customer_flag):
    if not customer_flag:
        dirpath = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(downnotbuy) + '\\' + str(percent) + str(
            stoploss) + '\\'
        finishlist_path = dirpath + 'finishedlist.csv'
        mkdir(dirpath)
        create_finished_list(finishlist_path)
    else:
        dirpath = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(downnotbuy) + '\\' + str(
            percent) + str(
            stoploss) + '\\'
        finishlist_path = dirpath + 'finishedlist.csv'
        mkdir(dirpath)
        create_finished_list(finishlist_path)
    for code in code_list:
        # path = get_path('multi' + str(downnotbuy)) + code + '.csv'
        path = dirpath + code + '.csv'
        # finishlist_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
        #     downnotbuy) + '\\' + 'finishedlist.csv'
        try:
            if not os.path.exists(path):
                first_run(code, percent, stoploss, downnotbuy, principal)
            else:
                not_first_run(code, percent, stoploss, downnotbuy, principal,customer_flag)
            print('正在回测' + code)
            # print(trade_flag_list)
            trade_flag_list.to_csv(path, index=False) #保存标志文件
            save_back_tocsv(code, winpercent, False)

            span_60_days = trade_flag_list.iloc[-61:]
            stock_num = span_60_days.iloc[0]['stock_num']
            price = span_60_days.iloc[0]['close']
            add_principal = sum(span_60_days['add_principal'].values.tolist())
            sum_principal = stock_num * price + add_principal
            end_price = span_60_days.iloc[-1]['close']
            end_principal = span_60_days.iloc[-1]['stock_num'] * end_price + span_60_days.iloc[-1]['principal']
            win_percent = round(((end_principal / sum_principal) - 1) * 100, 2)
            up_percent = round(((end_price / price) - 1) * 100, 2)
            diff_percent = round(win_percent - up_percent,2)
            trade_type = span_60_days.iloc[-1]['trade_type']
            span_days = str(span_60_days.iloc[0]['date']) + '-' + str(span_60_days.iloc[-1]['date'])
            name = get_name(code)

            write_to_csv(finishlist_path, [code,name,span_days,win_percent,up_percent,diff_percent,trade_type])
            finishlist_csv = pd.read_csv(finishlist_path).drop_duplicates(subset='code', keep='last')
            finishlist_csv.to_csv(finishlist_path, index=False)

            print(win_percent,up_percent,diff_percent,span_days,trade_type)
            trade_flag_list.drop(trade_flag_list.index, inplace=True)  # 清除trade_flag_list
            time.sleep(1)
        except Exception as e:
            traceback.print_exc()
            continue


def run_customer(start, end, code_list, percent, stoploss, downnotbuy, principal, winpercent):
    dirpath = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(downnotbuy) + '\\' + str(percent) + str(
        stoploss) + '\\'
    finishlist_path = dirpath + 'finishedlist.csv'
    mkdir(dirpath)
    create_finished_list(finishlist_path)
    for code in code_list:
        # path = get_path('customer' + str(downnotbuy)) + code + '.csv'
        path = dirpath + code + '.csv'
        # finishlist_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
        #     downnotbuy) + '\\' + 'finishedlist.csv'
        try:
            if not os.path.exists(path):
                first_run(code, percent, stoploss, downnotbuy, principal)
            else:
                not_first_run(start, end, code, percent, stoploss, downnotbuy, principal)
            print('正在回测' + code)
            trade_flag_list.to_csv(path, index=False)
            save_back_tocsv(code, winpercent, True)
            write_to_csv(finishlist_path, [code])
            finishlist_csv = pd.read_csv(finishlist_path).drop_duplicates(subset='code', keep='last')
            finishlist_csv.to_csv(finishlist_path, index=False)
            trade_flag_list.drop(trade_flag_list.index, inplace=True)
            time.sleep(1)
        except Exception as e:
            traceback.print_exc()
            continue


def save_back_tocsv(code, winpercent, customer_flag):
    csvpath = os.getcwd() + os.path.sep + 'saved_data' + '\\' + str(code).replace('.', '') + '.csv'
    if not os.path.exists(csvpath):
        global_data.to_csv(csvpath)
    else:
        old_df = pd.read_csv(csvpath, dtype={'trade_date': str}, index_col=0)
        # print(old_df)
        # new_gol = global_data.reset_index(drop=True)
        # print(new_gol)
        new_df = pd.concat([old_df, global_data.drop(labels=0)], ignore_index=True)
        # new_df = old_df.append(global_data).drop_duplicates(subset='trade_date',keep='last',inplace=False,ignore_index=True)
        new_df = new_df.drop_duplicates(subset='trade_date', keep='last', ignore_index=True)
        new_df = new_df.sort_values(by='trade_date', ascending=True, ignore_index=True)
        # print(global_data)
        # new_df = new_df.drop_duplicates(keep='first',ignore_index=True)
        new_df.to_csv(csvpath)
    # start_principal = sum(trade_flag_list['add_principal'].values.tolist())
    # end_principal = trade_flag_list.tail(1)['stock_num'].values[0] * trade_flag_list.tail(1)['close'].values[0] + \
    #                 trade_flag_list.tail(1)['principal'].values[0]
    # is_last_day_buy = False
    # if 0 < trade_flag_list.tail(1)['trade_type'].values[0] < 3:
    #     is_last_day_buy = True
    # # print(start_principal, end_principal)
    # if not customer_flag:
    #     csvpath = os.getcwd() + os.path.sep + 'multi' + '\\' + 'saved_data' + '\\' + str(code).replace('.', '') + '.csv'
    #     if end_principal >= (1 + winpercent) * start_principal or is_last_day_buy:
    #         if not os.path.exists(csvpath):
    #             global_data.to_csv(csvpath)
    #         else:
    #             old_df = pd.read_csv(csvpath)
    #             new_df = pd.concat([old_df,global_data.drop(labels=0)],ignore_index=True)
    #             new_df.to_csv(csvpath)
    # elif customer_flag:
    #     csvpath = os.getcwd() + os.path.sep + 'customer' + '\\' + 'saved_data' + '\\' + str(code).replace('.', '') + '.csv'
    #     if not os.path.exists(csvpath):
    #         global_data.to_csv(csvpath)
    #     else:
    #         old_df = pd.read_csv(csvpath)
    #         new_df = pd.concat([old_df, global_data.drop(labels=0)], ignore_index=True)
    #         new_df.to_csv(csvpath)

#
run(['600073.SH', '000005.SZ'], 0.1, 0.2, True, 100000, 0.1,False)
# run(['600073.SH', '000005.SZ'], 0.1, 0.2, True, 100000, 0.1,True)
# run_customer('20220707', '20230211', ['600073.SH', '000005.SZ'], 0.1, 0.2, True, 100000, 0.1)
# run_customer('20220707', '20230211', ['600073.SH'], 0.1, 0.2, True, 100000, 0.1)
