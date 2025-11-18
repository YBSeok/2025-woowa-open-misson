import pandas as pd
from ta.trend import WMAIndicator
from ta.volume import VolumeWeightedAveragePrice

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

try:
    df_org = df_org.rename(columns={
        'openingPrice': 'o',
        'highPrice': 'h',
        'lowPrice': 'l',
        'tradePrice': 'c',
        'candleAccTradeVolume': 'v'
    })
except Exception as e:
    print(f"컬럼명 변경 중 오류: {e}")
    exit()

df = df_org.iloc[df_org.shape[0]-144000:,].copy()
df['wma7'] = WMAIndicator(df['c'], window=7).wma()
df['wma99'] = WMAIndicator(df['c'], window=99).wma()
vwap = VolumeWeightedAveragePrice(high=df['h'], low=df['l'], close=df['c'], volume=df['v'], window=14)
df['vwap'] = vwap.volume_weighted_average_price()
df = df.dropna()

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
revenue_t = 0
buy_cnt_tot = 0

# 백테스팅 시작
print('----- Start back testing -----')
for i in range(0, df.shape[0] - 1):
    row = df.iloc[i]
    close1 = round(row['c'], 4)
    wma7 = round(row['wma7'], 4)
    wma99 = round(row['wma99'], 4)
    vwap = round(row['vwap'], 4)
    close2 = round(df.iloc[i + 1]['c'], 4)

    # 손실 최소화
    loss = buy_price - close2*buy_amt
    if loss > max_loss:
        revenue_t = close2 * buy_amt - buy_price - buy_price * trade_fee
        revenue = round(revenue + revenue_t,4)
        buy_cnt = 0
        buy_amt = 0
        buy_price = 0
        continue

    # 이익 실현
    tp_revenue = close2*buy_amt - (buy_price + buy_price*revenue_rate)
    if buy_cnt > 0 and tp_revenue > 0:
        revenue_t = close2*buy_amt - buy_price - buy_price * trade_fee
        revenue = round(revenue + revenue_t,4)
        buy_cnt = 0
        buy_amt = 0
        buy_price = 0
        continue


    # 포지션 오픈
    if buy_cnt < buy_cnt_limit and close2 < vwap and close2 < wma7 and wma7 > wma99:
        temp_amt = buy_amt_unit + buy_amt*increase_rate
        buy_price = round(buy_price + (close2 * temp_amt), 4)
        buy_amt = round(buy_amt + temp_amt, 4)
        buy_cnt = buy_cnt + 1
        buy_cnt_tot = buy_cnt_tot + 1

print('----- Back testing Finished -----')

unrealized_pnl = 0
final_revenue = revenue  # 1. 실현 손익으로 시작

# 2. 루프가 끝났을 때 아직 포지션을 들고 있는지 확인 (미실현 손익 계산)
if buy_cnt > 0:
    print(f"\n[알림] 테스트 종료 시점에 포지션 보유 중 (미실현 손익 정산)")
    last_price = df.iloc[-1]['c']  # 데이터의 가장 마지막 가격

    # 3. 현재 보유 포지션의 시장 가치 계산
    current_market_value = last_price * buy_amt

    # 4. 미실현 손익 (Unrealized P&L) 계산
    # (buy_price는 '총 매수 금액'으로 가정)
    unrealized_pnl = current_market_value - buy_price

    print(f"  > 보유 수량 (buy_amt): {buy_amt}")
    print(f"  > 총 매수 금액 (buy_price): {buy_price:.4f}")
    print(f"  > 현재 평가 금액: {current_market_value:.4f}")
    print(f"  > 미실현 손익: {unrealized_pnl:.4f}")

    # 5. 최종 수익 = 실현 수익 + 미실현 수익
    final_revenue = revenue + unrealized_pnl

# 6. 최종 결과 출력
print("\n----- Test results -----")
print(f"총 매수 진입 횟수: {buy_cnt_tot} 회")
print(f"실현 손익 (종료된 거래): {revenue:.4f}")
print(f"최종 총 손익 (미실현 포함): {final_revenue:.4f}")

# 7. 벤치마크: Buy & Hold (B&H) 수익률
first_price = df.iloc[0]['c']
last_price = df.iloc[-1]['c']
buy_and_hold_return = ((last_price - first_price) / first_price) * 100

print(f"\n----- 📊 벤치마크 (참고) -----")
print(f"Buy & Hold (B&H) 수익률: {buy_and_hold_return:.2f} %")
print(f"(첫날 가격: {first_price}, 마지막 날 가격: {last_price})")