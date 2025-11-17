from ta.trend import SMAIndicator
from ta.trend import WMAIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD
from ta.momentum import StochRSIIndicator
from ta.volatility import BollingerBands
from ta.volume import VolumeWeightedAveragePrice

df['sma7'] = SMAIndicator(df['c'], window=7).sma_indicator()
df['sma25'] = SMAIndicator(df['c'], window=25).sma_indicator()
df['sma60'] = SMAIndicator(df['c'], window=60).sma_indicator()
df.head(10)

df['wma7'] = WMAIndicator(df['c'], window=7).wma()
df['wma25'] = WMAIndicator(df['c'], window=25).wma()
df['wma60'] = WMAIndicator(df['c'], window=60).wma()
df.head(10)

df['ema7'] = EMAIndicator(df['c'], window=7).ema_indicator()
df['ema25'] = EMAIndicator(df['c'], window=25).ema_indicator()
df['ema60'] = EMAIndicator(df['c'], window=60).ema_indicator()
df.head(10)

macd = MACD(df['c'], window_slow=26, window_fast=12, window_sign=9)
df['macd'] = macd.macd()
df['macd_s'] = macd.macd_signal()
df['macd_d'] = macd.macd_diff()
df.tail(10)

stochRSI = StochRSIIndicator(df['c'], window=14, smooth1=3, smooth2=3)
df['srsi'] = stochRSI.stochrsi()
df['srsik'] = stochRSI.stochrsi_k()
df['srsid'] = stochRSI.stochrsi_d()
df.tail(10)

bb = BollingerBands(df['c'], window=20, window_dev=2)
df['bh'] = bb.bollinger_hband()
df['bhi'] = bb.bollinger_hband_indicator()
df['bl'] = bb.bollinger_lband()
df['bli'] = bb.bollinger_lband_indicator()
df['bm'] = bb.bollinger_mavg()
df['bw'] = bb.bollinger_wband()
df.tail(10)

vwap = VolumeWeightedAveragePrice(high=df['h'], low=df['l'], close=df['c'], volume=df['v'], window=14)
df['vwap'] = vwap.volume_weighted_average_price()
df.tail(10)

df = df.dropna()
df.colums
df.head(10)