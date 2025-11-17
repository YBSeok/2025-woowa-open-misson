import pandas as pd
import requests
import time
import random
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
    df_temp =  pd.read_json(webpage.text)

    df_temp_data = df_temp[cols]
    df_list.append(df_temp_data)

    temp_date = df_temp_data.tail(1)['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    start_time = temp_date.values[0]

    wait_time = random.choice([1.2, 1.4, 1.6, 1.8])
    time.sleep(wait_time)
    print(i, end=', ')

df_out = pd.concat(df_list, ignore_index=True)

df_out.to_csv("./{}.csv".format(coin_name), index=False)