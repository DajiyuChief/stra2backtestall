# -*- coding: utf-8 -*-
# @Time : 2023/3/4 21:06
# @Author : Dajiyu
# @File : client.py

import datetime
import json
import os.path
import socket

import pandas as pd

# remote server addr
# SERVER_IP = '127.0.0.1'
SERVER_IP = '172.29.7.161'
SERVER_PORT = 4321

# cache config
NO_CACHE = False
CACHE_DIR = os.path.dirname(__file__).replace('\\', '/') + '/cache/'

if not NO_CACHE:
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)


def get_data(code: str) -> pd.DataFrame:
    if NO_CACHE or cache_expired(code):
        return get_remote_data(code)
    else:
        return get_local_data(code)


def cache_expired(code: str):
    try:
        ts = os.path.getmtime(CACHE_DIR + code + '.csv')
    except FileNotFoundError:
        return True

    last = datetime.datetime.fromtimestamp(ts)
    current = datetime.datetime.today()
    if last.hour < 18 < current.hour:
        return True
    elif last.hour > 18 and current.day != last.day and current.hour > 18:
        return True
    return False


def get_remote_data(code: str) -> pd.DataFrame:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    client.sendall(code.encode())

    resp = ''
    while True:
        buf = client.recv(1024)
        if not buf:
            break
        resp += buf.decode()

    client.close()

    if resp:
        df = pd.DataFrame.from_dict(json.loads(resp))
        if not NO_CACHE:
            with open(CACHE_DIR + code + '.csv', 'wb') as f:
                df.to_csv(f, index=False)
        return df
    else:
        return pd.DataFrame()


def get_local_data(code) -> pd.DataFrame:
    try:
        return pd.read_csv(CACHE_DIR + code + '.csv')
    except FileNotFoundError:
        return pd.DataFrame()