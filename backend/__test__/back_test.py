import pandas as pd
from ta.trend import WMAIndicator
from ta.volume import VolumeWeightedAveragePrice
from comm.test_func import *
import itertools
import time
from bayes_opt import BayesianOptimization
import os

# -------------------------------------------------------------------
# 📈 [2] 데이터 로드 및 전처리 (1회 실행)
# -------------------------------------------------------------------
coin_name = "KRW-XRP"

try:
    file_path = f'data/{coin_name}.csv'
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

RESULTS_DIR = "data/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def prepare_data_for_saving(df, final_revenue, best_config):
    """
    최적의 파라미터로 시뮬레이션된 데이터프레임에서 필요한 정보를 추출
    """
    # 1. 최종 KPI 요약
    summary = {
        'final_revenue': final_revenue,
        'buy_and_hold_return': ((df.iloc[-1]['c'] - df.iloc[0]['c']) / df.iloc[0]['c']) * 100,
        'total_data_points': len(df),
        'best_config': best_config
    }
    
    # 2. 시계열 데이터 (차트용: 가격, 지표, 타임스탬프)
    chart_df = df.copy()
    chart_df['timestamp'] = chart_df.index.astype(str)
    
    return summary, chart_df[['timestamp', 'o', 'h', 'l', 'c', 'v', 'wma7', 'wma99', 'vwap']].iloc[-5000:,].copy()

# 지표 계산 (144000개 데이터 사용)
df = df_org.iloc[df_org.shape[0] - 144000:,].copy()
df['wma7'] = WMAIndicator(df['c'], window=7).wma()
df['wma99'] = WMAIndicator(df['c'], window=99).wma()
vwap_indicator = VolumeWeightedAveragePrice(high=df['h'], low=df['l'], close=df['c'], volume=df['v'], window=14)
df['vwap'] = vwap_indicator.volume_weighted_average_price()
df = df.dropna().reset_index(drop=True)


# -------------------------------------------------------------------
# 💻 [3] run_test 함수 정의
# -------------------------------------------------------------------

def run_test(config):
    revenue_rate = config['revenue_rate']
    max_loss_rate = config['max_loss_rate']
    increase_rate = config['increase_rate']
    buy_cnt_limit = int(config['buy_cnt_limit'])
    buy_amt_unit = config['buy_amt_unit']

    trade_fee = 0.001
    close = df.iloc[0]['c']

    max_loss = get_max_loss(close, buy_amt_unit, buy_cnt_limit, increase_rate, max_loss_rate)

    buy_cnt = 0
    buy_price = 0
    buy_amt = 0
    revenue = 0

    for i in range(0, df.shape[0] - 1):
        row = df.iloc[i]
        wma7 = row['wma7']
        wma99 = row['wma99']
        vwap = row['vwap']
        close2 = df.iloc[i + 1]['c']

        # 1. 손실 최소화 (Stop Loss)
        if buy_cnt > 0:
            loss_amount = buy_price - close2 * buy_amt
            if loss_amount > max_loss:
                revenue_t = close2 * buy_amt - buy_price - (buy_price * trade_fee)
                revenue = round(revenue + revenue_t, 4)
                buy_cnt = 0
                buy_amt = 0
                buy_price = 0
                continue

        # 2. 이익 실현 (Take Profit)
        if buy_cnt > 0:
            target_revenue_price = buy_price * (1 + revenue_rate)
            tp_revenue = close2 * buy_amt - target_revenue_price

            if tp_revenue > 0:
                revenue_t = close2 * buy_amt - buy_price - (buy_price * trade_fee)
                revenue = round(revenue + revenue_t, 4)
                buy_cnt = 0
                buy_amt = 0
                buy_price = 0
                continue

        # 3. 포지션 오픈/추가 매수 (Entry/Add Position)
        if buy_cnt < buy_cnt_limit and close2 < vwap and close2 < wma7 and wma7 > wma99:
            temp_amt = buy_amt_unit + buy_amt * increase_rate
            new_buy_price = buy_price + (close2 * temp_amt)
            buy_price = round(new_buy_price, 4)
            buy_amt = round(buy_amt + temp_amt, 4)
            buy_cnt = buy_cnt + 1

    # 테스트 종료 시 미실현 손익 정산
    final_revenue = revenue
    if buy_cnt > 0:
        last_price = df.iloc[-1]['c']
        current_market_value = last_price * buy_amt
        unrealized_pnl = current_market_value - buy_price
        final_revenue = revenue + unrealized_pnl

    return final_revenue


# -------------------------------------------------------------------
# ⚙️ [4] 최적화 탐색
# -------------------------------------------------------------------

start_time = time.time()
all_results_for_bayes = []

## 그리드 서치 (Warm Start 데이터 수집)
grid_param_space = {
    'revenue_rate': [0.008, 0.014, 0.020],
    'max_loss_rate': [0.1, 0.2, 0.3],
    'increase_rate': [0.1, 0.2, 0.3],
    'buy_cnt_limit': [5, 7, 10],
    'buy_amt_unit': [4.5, 8.0, 12.0],
}

keys = grid_param_space.keys()
combinations = itertools.product(*grid_param_space.values())
grid_configs = [dict(zip(keys, c)) for c in combinations]

print(f"--- 📊 1단계: 그리드 서치 (Warm Start 데이터 수집) 시작 (총 {len(grid_configs)}개) ---")

for config in grid_configs:
    try:
        final_revenue = run_test(config)

        data_point = {
            'revenue_rate': config['revenue_rate'],
            'max_loss_rate': config['max_loss_rate'],
            'increase_rate': config['increase_rate'],
            'buy_cnt_limit': float(config['buy_cnt_limit']),
            'buy_amt_unit': config['buy_amt_unit'],
            'target': final_revenue
        }
        all_results_for_bayes.append(data_point)

    except Exception as e:
        pass

grid_results_df = pd.DataFrame(all_results_for_bayes)
if not grid_results_df.empty:
    print("--- ✅ 그리드 서치 완료 (Warm Start 데이터 준비) ---")
    best_grid_revenue = grid_results_df['target'].max()
    print(f"최고 그리드 수익: {best_grid_revenue:.4f}")
else:
    print("--- ⚠️ 그리드 서치 결과 없음 ---")

print("-" * 50)


## 베이지안 최적화 (Warm Start 적용)

def black_box_function(revenue_rate, max_loss_rate, increase_rate, buy_cnt_limit, buy_amt_unit):
    buy_cnt_limit = int(round(buy_cnt_limit))

    config_data = {
        'revenue_rate': revenue_rate,
        'max_loss_rate': max_loss_rate,
        'increase_rate': increase_rate,
        'buy_cnt_limit': buy_cnt_limit,
        'buy_amt_unit': buy_amt_unit
    }

    revenue = run_test(config_data)

    return revenue




pbounds = {
    'revenue_rate': (0.005, 0.025),
    'max_loss_rate': (0.05, 0.40),
    'increase_rate': (0.1, 0.5),
    'buy_cnt_limit': (5, 15),
    'buy_amt_unit': (4, 20),
}

optimizer = BayesianOptimization(
    f=black_box_function,
    pbounds=pbounds,
    random_state=1,
)

# 그리드 서치 결과를 베이지안 최적화 모델에 주입 (Warm Start)
if not grid_results_df.empty:
    for index, row in grid_results_df.iterrows():
        try:
            # 베이지안 모델에 (파라미터, 수익) 데이터 주입
            optimizer.register(
                params={k: row[k] for k in pbounds.keys()},
                target=row['target']
            )
        except Exception:
            # 경계 밖의 값이 있을 경우 무시하고 다음 값 진행
            pass
    print(f"--- 🧠 2단계: 베이지안 최적화 시작 (Warm Start 데이터 {len(optimizer.space)}개 주입 완료) ---")
else:
    print(f"--- 🧠 2단계: 베이지안 최적화 시작 (Warm Start 데이터 없이 시작) ---")

# 최적화 실행 (Warm Start 데이터 개수만큼 init_points를 줄임)
ITERATIONS = 50
optimizer.maximize(
    init_points=0,  # Warm Start를 했으므로 무작위 초기 탐색 횟수를 0으로 설정
    n_iter=ITERATIONS,
)

print("--- ✅ 베이지안 최적화 완료 ---")

# 최종 결과 출력
best_params = optimizer.max['params']
best_revenue = optimizer.max['target']

# buy_cnt_limit을 정수 변환
best_params['buy_cnt_limit'] = int(round(best_params['buy_cnt_limit']))

final_best_config = best_params.copy() 

print("-" * 50)
print(f"총 실행 시간: {time.time() - start_time:.2f}초")

print("\n==============================================")
print("🏆 최종 최적의 알고리즘 파라미터 (하이브리드 최적화)")
print("==============================================")
print(f"**최대 최종 수익:** {best_revenue:.4f}")
print("\n**최적 Config:**")
for k, v in best_params.items():
    print(f"  - {k}: {v}")
print("==============================================")


try:
    print("\n--- 💾 최종 최적화 결과로 백테스팅 재실행 및 파일 저장 ---")

    summary, chart_df = prepare_data_for_saving(df, best_revenue, final_best_config)

    test_id = f"optimal_run_{int(time.time())}" 
    
    save_backtest_results(test_id, summary, chart_df)

    print(f"\n[✔️ 연동 준비 완료] 프론트엔드는 '/api/backtest/results/{test_id}' 경로로 요청하여 데이터를 불러올 수 있습니다.")

except Exception as e:
    print(f"[❌ 저장 오류] 파일 저장 중 오류가 발생했습니다: {e}")