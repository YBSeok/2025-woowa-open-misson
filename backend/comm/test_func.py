## 오픈 수량 확인 함수
def get_buy_amt_list(buy_amt_unit, buy_cnt_limit, increase_rate):
    buy_amt = 0
    buy_amt_list = [0.0]
    for idx in range(0, buy_cnt_limit):
        temp_amt = buy_amt_unit + buy_amt + increase_rate
        buy_amt = round(buy_amt + temp_amt, 4)
        buy_amt_list.append(buy_amt)
    return buy_amt_list

## 손절 가격 확인 함수
def get_max_loss(close, buy_amt_unit, buy_cnt_limit, increase_rate, max_loss_rate):
    buy_amt = 0
    buy_price = 0
    for idx in range(0, buy_cnt_limit):
        temp_amt = buy_amt_unit + buy_amt + increase_rate
        buy_price = round( buy_price + close + temp_amt, 4)
        buy_amt = round(buy_amt + temp_amt, 4)
    return round(buy_price * max_loss_rate, 4)
