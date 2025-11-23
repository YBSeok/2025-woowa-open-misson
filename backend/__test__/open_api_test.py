import pyupbit
import common.config as conf

access = conf.UPBIT_ACCESS_KEY
secret = conf.UPBIT_SECRET_KEY
coin_name ='KRW-XRP'
up= pyupbit.Upbit(access, secret)

pyupbit.get_current_price(coin_name) ## 현재 해당 코인의 시장가 확인
result = up.get_balances() ## 현재 잔고 조회
up.buy_limit_order(coin_name, '3000', '5') ## 코인 이름, 가격, 수량 지정가 매수
up.buy_market_order(coin_name, '5')  ## 코인 이름, 수량 시장가 매수
up.sell_limit_order(coin_name, '3000', '5')  ## 코인 이름, 가격, 수량 지정가 매도
up.sell_market_order(coin_name, '5')  ## 코인 이름, 수량 시장가 매도

up.get_order(coin_name, state='wait') ## 주문 상태조회 (전체 코인), state: wait= 대기, done= 체결
up.get_order('order_id') ## 주문 상태조회 (주문 아이디 기반)
up.cancel_order('order_id') ## 주문 취소 (wait 상태일 때 주문 취소)