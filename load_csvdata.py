import pandas as pd
import os
from baseFun import get_need_data, get_name


# from getstockname import get_name


def load_finished_code(rsi, stoploss, downnotbuy, type,middleadd):
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
    # 显示收益率达到要求的代码
    rsi = str(rsi)
    stoploss = str(stoploss)
    dirpath = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(downnotbuy) + '\\' + str(
        percnet) + str(
        stoploss) + str(middleadd)+ '\\' + start + end + '\\'
    csv_path = dirpath + 'finishedlist.csv'
    # if not type:
    #     csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
    #         downnotbuy) + '\\' + rsi + stoploss + '\\' + 'finishedlist.csv'
    # elif type:
    #     csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
    #         downnotbuy) + '\\' + rsi + stoploss + '\\' + 'finishedlist.csv'
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
def load_today_buy(rsi, stoploss,downnotbuy,middleadd):
    rsi = str(rsi)
    stoploss = str(stoploss)
    csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
        downnotbuy) + '\\' + rsi + stoploss +str(middleadd)+ '\\' + 'finishedlist.csv'
    finish_csv = pd.read_csv(csv_path)
    satisfied_csv = finish_csv[finish_csv['trade_type'] > 0]
    if satisfied_csv.empty:
        return []
    return satisfied_csv.values.tolist()
# load_winning_code(0.1,0.2,-10,True,False)