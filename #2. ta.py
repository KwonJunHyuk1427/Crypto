import ccxt
import pandas as pd
from datetime import datetime
from ta.trend import SMAIndicator, PSARIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.momentum import StochRSIIndicator
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

#API
binance = ccxt.binance({
    'apiKey': '', 
    'secret': '',
})
binance.options['createMarketBuyOrderRequiresPrice'] = False

#Basic
bars = binance.fetch_ohlcv('BTC/BUSD', timeframe='5m', since=None, limit=None)
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] += 32400000
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

#Moving Average
simpleMA = SMAIndicator(df['close'], window=100)
df['sma'] = simpleMA.sma_indicator()

#ParabolicSAR
parabolicSAR = PSARIndicator(df['high'], df['low'], df['close'])
df['psar'] = parabolicSAR.psar()
df['psar_u'] = parabolicSAR.psar_up()
df['psar_d'] = parabolicSAR.psar_down()
df['psar_ui'] = parabolicSAR.psar_up_indicator()
df['psar_di'] = parabolicSAR.psar_down_indicator()

#Bollingerband
bb_indicator = BollingerBands(df['close'])
df['upperband'] = bb_indicator.bollinger_hband()
df['lowerband'] = bb_indicator.bollinger_lband()
df['moving_average'] = bb_indicator.bollinger_mavg()

#ATR
atr_indicator = AverageTrueRange(df['high'], df['low'], df['close'])
df['atr'] = atr_indicator.average_true_range()

#StochasticRSI
stochRSI = StochRSIIndicator(df['close'])
df['srsi'] = stochRSI.stochrsi()
df['srsi_k'] = stochRSI.stochrsi_k()
df['srsi_d'] = stochRSI.stochrsi_d()