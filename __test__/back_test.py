import pandas as pd
from comm.test_func import get_buy_amt_list, get_max_loss

coin_name = "KRW-XRP"

try:
    file_path = f'../data/{coin_name}.csv'
    df_org = pd.read_csv(file_path)

except FileNotFoundError:
    print(f"오류: '{file_path}' file not found")
    exit()
except Exception as e:
    print(f"Data load error: {e}")
    exit()

revenue_rate = 0.014
max_loss_rate = 0.2
increase_rate = 0.2
buy_cnt_limit = 7
buy_amt_unit = 4.5
trade_fee = 0.001
close = 1300
buy_amt_list = get_buy_amt_list(buy_amt_unit, buy_cnt_limit, increase_rate)
max_loss = get_max_loss(close, buy_amt_unit, buy_cnt_limit, increase_rate, max_loss_rate)

buy_cnt = 0
buy_price = 0
buy_amt = 0
revenue = 0
revenue_total = 0

df = df_org.iloc[df_org.shape[0]-144000:,]

for i in range(0, df.shape[0]-1):
    close1 = round(df.iloc[i:i+1,]['c'].values[0], 4)
    close2 = round(df.iloc[i+1:i+2,]['c'].values[0], 4)
    wma7 = round(df.iloc[i:i+1,]['wma7'].values[0], 4)
    wma99 = round(df.iloc[i:i+1,]['wma99'].values[0], 4)
    vwap = round(df.iloc[i:i+1,]['vwap'].values[0], 4)