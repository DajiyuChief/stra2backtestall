import pandas as pd
import os
from baseFun import get_need_data, get_name


# from getstockname import get_name


def load_finished_code(rsi, stoploss, downnotbuy, type):
    # 显示已完成回测的代码
    rsi = str(rsi)
    stoploss = str(stoploss)
    if not type:
        csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
            downnotbuy) + '\\' + rsi + stoploss + '\\' + 'finishedlist.csv'
    elif type:
        csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
            downnotbuy) + '\\' + rsi + stoploss + '\\' + 'finishedlist.csv'
    if not os.path.exists(csv_path):
        return []
    # df = pd.read_csv('back_all.csv')
    df = pd.read_csv(csv_path)
    if len(df) <= 1:
        return []
    finished_list = sorted(list(set(df['code'].values.tolist())))
    return finished_list


def load_winning_code(rsi, stoploss, percnet, downnotbuy, type):
    # 显示收益率达到要求的代码
    rsi = str(rsi)
    stoploss = str(stoploss)
    if not type:
        csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
            downnotbuy) + '\\' + rsi + stoploss + '\\' + 'finishedlist.csv'
    elif type:
        csv_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'customer' + str(
            downnotbuy) + '\\' + rsi + stoploss + '\\' + 'finishedlist.csv'
    if not os.path.exists(csv_path):
        return []
    df = pd.read_csv(csv_path)
    if df.empty:
        return []
    finished_list = load_finished_code(rsi, stoploss, downnotbuy, type)
    satisfied_list = []
    if not type:
        finish_csv = pd.read_csv(csv_path).drop_duplicates(subset='code', keep='last')
        # finishlist_csv = pd.read_csv(finishlist_path).drop_duplicates(subset='code', keep='last')
        # finishlist_csv.to_csv(finishlist_path, index=False)
        satisfied_csv = finish_csv[finish_csv['win_percent'] >= percnet*100]
    elif type:
        finish_csv = pd.read_csv(csv_path).drop_duplicates(subset='code', keep='last')
        satisfied_csv = finish_csv
    # print(satisfied_csv.values.tolist())
    # if not type:
    #     saved_dir_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'saved_data'
    # else:
    #     saved_dir_path = os.getcwd() + os.path.sep + 'customer' + '\\' + 'saved_data'
    # if type:
    #     customer_code = pd.read_csv(os.getcwd() + os.path.sep + 'customer' + '\\' + 'custmoerlist.csv')[
    #         'code'].values.tolist()
    #     finished_list1 = list(set(finished_list).intersection(customer_code))
    #     finished_list = finished_list1
    # for code in finished_list:
    #     data = df[df['code'] == code]
    #     principal_list = data['principal'].values.tolist()
    #     if not type and (principal_list[-1] > principal_list[0] * (1 + percnet)):
    #         trans_csv_path = saved_dir_path + '\\' + code.replace('.', '') + '.csv'
    #         real_data = get_need_data(trans_csv_path, start, end, 0, 0)
    #         win_percent = round((principal_list[-1] - principal_list[0]) * 100 / principal_list[0], 2)
    #         up_percent = (real_data['close'].values.tolist()[-1] - real_data['close'].values.tolist()[0]) * 100 / \
    #                      real_data['close'].values.tolist()[0]
    #         diff = win_percent - round(up_percent, 2)
    #         span = str(start) + '-' + str(end)
    #         satisfied_list.append([code, get_name(code), span, win_percent, round(up_percent, 2), round(diff, 2)])
    #     elif type:
    #         trans_csv_path = saved_dir_path + '\\' + code.replace('.', '') + '.csv'
    #         real_data = get_need_data(trans_csv_path, start, end, 0, 0)
    #         win_percent = round((principal_list[-1] - principal_list[0]) * 100 / principal_list[0], 2)
    #         up_percent = (real_data['close'].values.tolist()[-1] - real_data['close'].values.tolist()[0]) * 100 / \
    #                      real_data['close'].values.tolist()[0]
    #         diff = win_percent - round(up_percent, 2)
    #         span = str(start) + '-' + str(end)
    #         satisfied_list.append([code, get_name(code), span, win_percent, round(up_percent, 2), round(diff, 2)])

    return satisfied_csv.values.tolist()

def load_today_buy(rsi, stoploss,downnotbuy):
    rsi = str(rsi)
    stoploss = str(stoploss)
    csv_path = os.getcwd() + os.path.sep + 'multi' + '\\' + 'multi' + str(
        downnotbuy) + '\\' + rsi + stoploss + '\\' + 'finishedlist.csv'
    finish_csv = pd.read_csv(csv_path)
    satisfied_csv = finish_csv[finish_csv['trade_type'] > 0]
    if satisfied_csv.empty:
        return []
    return satisfied_csv.values.tolist()
# load_winning_code(0.1,0.2,-10,True,False)