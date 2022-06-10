import ccxt
import pandas as pd
from datetime import datetime
from ta.trend import SMAIndicator, PSARIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.momentum import StochRSIIndicator
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

#Tickers
binance = ccxt.binance()
markets = binance.fetch_tickers()
for keys in markets:
    print(keys)

#Current Data
binance = ccxt.binance()
ticker = binance.fetch_ticker('BTC/BUSD')
print(ticker['open'], ticker['high'], ticker['low'], ticker['close'])

#Past Data
binance = ccxt.binance()
ohlcvs = binance.fetch_ohlcv('BTC/BUSD',timeframe='5m', since=None, limit=None)
for ohlc in ohlcvs:
    print(datetime.fromtimestamp(ohlc[0]/1000).strftime('%Y-%m-%d %H:%M:%S'), ohlc[1:])

#Order Book
binance = ccxt.binance()
orderbook = binance.fetch_order_book('BTC/BUSD', limit=None)
for bid in orderbook['bids']:
    print(bid[0], bid[1])
for ask in orderbook['asks']:
    print(ask[0], ask[1])

#Balance
binance = ccxt.binance({
    'apiKey': '', 
    'secret': '',
})
balance = binance.fetch_balance()
print(balance.keys())
print(balance['BTC']['free'], balance['BTC']['used'], balance['BTC']['total'])
print(balance['BUSD']['free'], balance['KRW']['used'], balance['KRW']['total'])

#Buy and Sell
binance = ccxt.binance({
    'apiKey': '', 
    'secret': '',
})
binance.options['createMarketBuyOrderRequiresPrice'] = False
order = binance.create_limit_buy_order('BTC/BUSD', 'COIN', 'KRW')
print(order)
order = binance.create_limit_sell_order('BTC/BUSD', 'COIN', 'KRW')
print(order)
order = binance.create_market_buy_order('BTC/BUSD', 'KRW')
print(order)
order = binance.create_market_sell_order('BTC/BUSD', 'COIN')
print(order)

#Order Confirm
resp = binance.fetch_order('orderid', 'BTC/BUSD')
print(resp)

#Order Cancel
resp = binance.cancel_order('orderid', 'BTC/BUSD')
print(resp)