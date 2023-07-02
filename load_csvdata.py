import datetime

import pandas as pd
import os
from baseFun import get_need_data, get_name


# from getstockname import get_name


def load_finished_code(rsi, stoploss, downnotbuy, type,middleadd):
    '''
    显示已完成回测的代码
    :param rsi:
    :param stoploss:
    :param downnotbuy:
    :param type:
    :param middleadd:
    :return:
    '''
    # 显示已完成回测的代码
    rsi = str(rsi)
    stoploss = str(stoploss)
    if not type:
        csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
            downnotbuy) + '\\' + rsi + stoploss +str(middleadd)+ '\\' + 'finishedlist.csv'
    elif type:
        csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
            downnotbuy) + '\\' + rsi + stoploss + str(middleadd)+'\\' + 'finishedlist.csv'
    if not os.path.exists(csv_path):
        return []
    # df = pd.read_csv('back_all.csv')
    df = pd.read_csv(csv_path)
    if len(df) <= 1:
        return []
    finished_list = sorted(list(set(df['code'].values.tolist())))
    return finished_list


def load_winning_code(rsi, stoploss, percnet, downnotbuy, type,middleadd):
    '''
     显示收益率达到要求的代码
    :param rsi:
    :param stoploss:
    :param percnet:
    :param downnotbuy:
    :param type:
    :param middleadd:
    :return:
    '''
    # 显示收益率达到要求的代码
    rsi = str(rsi)
    stoploss = str(stoploss)
    if not type:
        csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
            downnotbuy) + '\\' + rsi + stoploss + str(middleadd)+ '\\' + 'finishedlist.csv'
    elif type:
        csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
            downnotbuy) + '\\' + rsi + stoploss + str(middleadd)+'\\' + 'finishedlist.csv'
    if not os.path.exists(csv_path):
        return []
    df = pd.read_csv(csv_path)
    if df.empty:
        return []
    finished_list = load_finished_code(rsi, stoploss, downnotbuy, type,middleadd)
    satisfied_list = []
    if not type:
        finish_csv = pd.read_csv(csv_path).drop_duplicates(subset='code', keep='last')
        # finishlist_csv = pd.read_csv(finishlist_path).drop_duplicates(subset='code', keep='last')
        # finishlist_csv.to_csv(finishlist_path, index=False)
        satisfied_csv = finish_csv[finish_csv['win_percent'] >= percnet*100]
    elif type:
        finish_csv = pd.read_csv(csv_path).drop_duplicates(subset='code', keep='last')
        satisfied_csv = finish_csv

    return satisfied_csv.values.tolist()


def load_winning_code_customer(start,end,rsi, stoploss, percnet, downnotbuy, type,middleadd):
    '''
    显示收益率达到要求的代码
    :param start:
    :param end:
    :param rsi:
    :param stoploss:
    :param percnet:
    :param downnotbuy:
    :param type:
    :param middleadd:
    :return:
    '''
    # 显示收益率达到要求的代码
    rsi = str(rsi)
    stoploss = str(stoploss)
    dirpath = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(downnotbuy) + '\\' + str(
        percnet) + str(
        stoploss) + str(middleadd)+ '\\'
    csv_path = dirpath + 'finishedlist.csv'
    if not os.path.exists(csv_path):
        return []
    df = pd.read_csv(csv_path)
    if df.empty:
        return []
    if not type:
        finish_csv = pd.read_csv(csv_path).drop_duplicates(subset='code', keep='last')
        satisfied_csv = finish_csv[finish_csv['win_percent'] >= percnet*100]
    elif type:
        finish_csv = pd.read_csv(csv_path).drop_duplicates(subset='code', keep='last')
        satisfied_csv = finish_csv
    # print(satisfied_csv.values.tolist())
    return satisfied_csv.values.tolist()

def load_today_buy(rsi, stoploss,downnotbuy,middleadd):
    '''
    筛选今日可买股票
    :param rsi:
    :param stoploss:
    :param downnotbuy:
    :param middleadd:
    :return:
    '''
    today = datetime.datetime.today().strftime('%Y%m%d')
    rsi = str(rsi)
    stoploss = str(stoploss)
    csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
        downnotbuy) + '\\' + rsi + stoploss +str(middleadd)+ '\\' + 'finishedlist.csv'
    if not os.path.exists(csv_path):
        return []
    finish_csv = pd.read_csv(csv_path)
    satisfied_csv = finish_csv[finish_csv['trade_type'] > 0]
    satisfied_csv = satisfied_csv[satisfied_csv['trade_type'] < 3]
    # satisfied_csv = satisfied_csv[satisfied_csv['span'].str.split('-')[1] == today]
    satisfied_csv['end_date'] = satisfied_csv['span'].apply(lambda x:str(x).split('-')[1])
    satisfied_csv = satisfied_csv[satisfied_csv['end_date'] == today]
    satisfied_csv = satisfied_csv.drop_duplicates(keep='last',inplace=False)
    if satisfied_csv.empty:
        return []
    return satisfied_csv.values.tolist()

def load_today_winning_code_customer(rsi, stoploss, downnotbuy, middleadd):
    '''
    筛选今日达到收益要求股票
    :param rsi:
    :param stoploss:
    :param downnotbuy:
    :param middleadd:
    :return:
    '''
    stoploss = str(stoploss)
    dirpath = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(downnotbuy) + '\\' + str(
        rsi) + str(
        stoploss) + str(middleadd) + '\\' + 'realtime' + '\\'
    csv_path = dirpath + 'finishedlist.csv'
    if not os.path.exists(csv_path):
        return []
    satisfied_code_win_name = pd.read_csv(csv_path)
    if satisfied_code_win_name.empty:
        return []
    finish_csv = pd.read_csv(csv_path).drop_duplicates(subset='code', keep='last')
    satisfied_csv = finish_csv
    # print(satisfied_csv.values.tolist())
    return satisfied_csv.values.tolist()