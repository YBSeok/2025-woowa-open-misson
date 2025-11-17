import pandas as pd
import numpy as np
import requests
import csv
import time
import random
import datetime
import os
import warnings

warnings.filterwarnings(action="ignore")

coin_name= "KRW-XRP"
start_time = "2025-11-15T10:00:00"
base_url = "https://crix-api-cdn.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.{}&count=400&to={}.000Z"
cols = ['timestamp','openingPrice', 'highPrice', 'lowPrice', 'tradePrice', 'candleAccTradeVolume']
df_out = pd.DataFrame()

df_list = []
for i in range(0,500):
    url = base_url.format(coin_name, start_time)
    webpage = requests.get(url)
    df_temp =  pd.read_json(webpage.text) # 2. (이전 에러 수정) .content -> .text

    df_temp_data = df_temp[cols]
    df_list.append(df_temp_data) # 3. df_out.append 대신 리스트에 추가합니다.

    temp_date = df_temp_data.tail(1)['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    start_time = temp_date.values[0]

    wait_time = random.choice([1.2, 1.4, 1.6, 1.8])
    time.sleep(wait_time)
    print(i, end=', ')

# 5. 루프가 모두 끝난 후, 리스트를 DataFrame으로 한 번에 합칩니다.
df_out = pd.concat(df_list, ignore_index=True)

# 6. 최종 결과를 파일로 한 번만 저장합니다.
df_out.to_csv("./{}.csv".format(coin_name), index=False)