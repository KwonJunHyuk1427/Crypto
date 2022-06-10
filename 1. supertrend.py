import ccxt
import pandas as pd
import numpy as np
import schedule
import time
import random
import warnings
from datetime import datetime
from ta.volatility import AverageTrueRange
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
warnings.filterwarnings('ignore')

#API
binance = ccxt.binance({
    'apiKey': '', 
    'secret': '',
})
binance.options['createMarketBuyOrderRequiresPrice'] = False

#Settings
position = False
price = 0
count = 0

#Supertrend
def supertrend(df, multiplier=3):
    atr_indicator = AverageTrueRange(df['high'], df['low'], df['close'])
    df['atr'] = atr_indicator.average_true_range()
    df['upperband'] = ((df['high'] + df['low']) / 2) + (multiplier * df['atr'])
    df['lowerband'] = ((df['high'] + df['low']) / 2) - (multiplier * df['atr'])
    df['uptrend'] = False
    for current in range(1, len(df.index)):
        previous = current - 1
        if df['close'][current] > df['upperband'][previous]:
            df['uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['uptrend'][current] = False
        else:
            df['uptrend'][current] = df['uptrend'][previous]
            if df['uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]
            if not df['uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]
    return df

#Signals
def signals(df):
    global position
    global price
    global count
    current = len(df.index) - 1
    previous = len(df.index) - 2
    print(df['keys'][current])
    #RG
    if not df['uptrend'][previous] and df['uptrend'][current]:
        if position:
            print('now uptrend')
            count = random.randrange(0,3)
        if not position:
            print('now uptrend')
            count = random.randrange(0,3)
    #GR
    if df['uptrend'][previous] and not df['uptrend'][current]:
        if position:
            sell(df)
            print('now downtrend')
            count = random.randrange(0,3)
        if not position:
            print('now downtrend')
            count = random.randrange(0,3)
    #RR
    if not df['uptrend'][previous] and not df['uptrend'][current]:
        if position:
            sell(df)
            print('red line')
            count = random.randrange(0,3)
        if not position:
            print('red waiting')
            count = random.randrange(0,3)
    #GG
    if df['uptrend'][previous] and df['uptrend'][current]:
        if position:
            if price * 1.500 < df['close'][current]:
                sell(df)
                print('far line')
                count = random.randrange(0,3)
            else:
                print('sell waiting')
                count += 0
                time.sleep(240)
        if not position:
            if df['lowerband'][current] * 1.005 > df['close'][current]:
                buy(df)
                print('near line')
                count += 0
                time.sleep(240)
            else:
                print('buy waiting')
                count = random.randrange(0,3)

#Buy
def buy(df):
    global position
    global price
    global count
    current = len(df.index) - 1
    previous = len(df.index) - 2
    binance.create_market_buy_order(df['keys'][current], df['maxusdt'][current] * 0.999)
    position = True
    price = df['close'][current]

#Sell
def sell(df):
    global position
    global price
    global count
    current = len(df.index) - 1
    previous = len(df.index) - 2
    binance.create_market_sell_order(df['keys'][current], df['maxcoin'][current])
    position = False
    price = 0

#Run
def run_bot():
    #Tickers
    keys = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'BCC/USDT', 'NEO/USDT', 'LTC/USDT', 'QTUM/USDT', 'ADA/USDT', 'XRP/USDT', 'EOS/USDT', 'TUSD/USDT', 'IOTA/USDT', 'XLM/USDT', 'ONT/USDT', 'TRX/USDT', 'ETC/USDT', 'ICX/USDT', 'VEN/USDT', 'NULS/USDT', 'VET/USDT', 'PAX/USDT', 'BCH/USDT', 'BSV/USDT', 'USDC/USDT', 'LINK/USDT', 'WAVES/USDT', 'BTT/USDT', 'USDS/USDT', 'ONG/USDT', 'HOT/USDT', 'ZIL/USDT', 'ZRX/USDT', 'FET/USDT', 'BAT/USDT', 'XMR/USDT', 'ZEC/USDT', 'IOST/USDT', 'CELR/USDT', 'DASH/USDT', 'NANO/USDT', 'OMG/USDT', 'THETA/USDT', 'ENJ/USDT', 'MITH/USDT', 'MATIC/USDT', 'ATOM/USDT', 'TFUEL/USDT', 'ONE/USDT', 'FTM/USDT', 'ALGO/USDT', 'USDSB/USDT', 'GTO/USDT', 'ERD/USDT', 'DOGE/USDT', 'DUSK/USDT', 'ANKR/USDT', 'WIN/USDT', 'COS/USDT', 'NPXS/USDT', 'COCOS/USDT', 'MTL/USDT', 'TOMO/USDT', 'PERL/USDT', 'DENT/USDT', 'MFT/USDT', 'KEY/USDT', 'STORM/USDT', 'DOCK/USDT', 'WAN/USDT', 'FUN/USDT', 'CVC/USDT', 'CHZ/USDT', 'BAND/USDT', 'BUSD/USDT', 'BEAM/USDT', 'XTZ/USDT', 'REN/USDT', 'RVN/USDT', 'HC/USDT', 'HBAR/USDT', 'NKN/USDT', 'STX/USDT', 'KAVA/USDT', 'ARPA/USDT', 'IOTX/USDT', 'RLC/USDT', 'MCO/USDT', 'CTXC/USDT', 'TROY/USDT', 'VITE/USDT', 'FTT/USDT', 'EUR/USDT', 'OGN/USDT', 'DREP/USDT', 'BULL/USDT', 'BEAR/USDT', 'ETHBULL/USDT', 'ETHBEAR/USDT', 'TCT/USDT', 'WRX/USDT', 'BTS/USDT', 'LSK/USDT', 'BNT/USDT', 'LTO/USDT', 'EOSBULL/USDT', 'EOSBEAR/USDT', 'XRPBULL/USDT', 'XRPBEAR/USDT', 'STRAT/USDT', 'AION/USDT', 'MBL/USDT', 'COTI/USDT', 'BNBBULL/USDT', 'BNBBEAR/USDT', 'STPT/USDT', 'WTC/USDT', 'DATA/USDT', 'XZC/USDT', 'SOL/USDT', 'CTSI/USDT', 'HIVE/USDT', 'CHR/USDT', 'BTCUP/USDT', 'BTCDOWN/USDT', 'GXS/USDT', 'ARDR/USDT', 'LEND/USDT', 'MDT/USDT', 'STMX/USDT', 'KNC/USDT', 'REP/USDT', 'LRC/USDT', 'PNT/USDT', 'COMP/USDT', 'BUSDT/USDT', 'SC/USDT', 'ZEN/USDT', 'SNX/USDT', 'ETHUP/USDT', 'ETHDOWN/USDT', 'ADAUP/USDT', 'ADADOWN/USDT', 'LINKUP/USDT', 'LINKDOWN/USDT', 'VTHO/USDT', 'DGB/USDT', 'GBP/USDT', 'SXP/USDT', 'MKR/USDT', 'DAI/USDT', 'DCR/USDT', 'STORJ/USDT', 'BNBUP/USDT', 'BNBDOWN/USDT', 'XTZUP/USDT', 'XTZDOWN/USDT', 'MANA/USDT', 'AUD/USDT', 'YFI/USDT', 'BAL/USDT', 'BLZ/USDT', 'IRIS/USDT', 'KMD/USDT', 'JST/USDT', 'SRM/USDT', 'ANT/USDT', 'CRV/USDT', 'SAND/USDT', 'OCEAN/USDT', 'NMR/USDT', 'DOT/USDT', 'LUNA/USDT', 'RSR/USDT', 'PAXG/USDT', 'WNXM/USDT', 'TRB/USDT', 'BZRX/USDT', 'SUSHI/USDT', 'YFII/USDT', 'KSM/USDT', 'EGLD/USDT', 'DIA/USDT', 'RUNE/USDT', 'FIO/USDT', 'UMA/USDT', 'EOSUP/USDT', 'EOSDOWN/USDT', 'TRXUP/USDT', 'TRXDOWN/USDT', 'XRPUP/USDT', 'XRPDOWN/USDT', 'DOTUP/USDT', 'DOTDOWN/USDT', 'BEL/USDT', 'WING/USDT', 'LTCUP/USDT', 'LTCDOWN/USDT', 'UNI/USDT', 'NBS/USDT', 'OXT/USDT', 'SUN/USDT', 'AVAX/USDT', 'HNT/USDT', 'FLM/USDT', 'UNIUP/USDT', 'UNIDOWN/USDT', 'ORN/USDT', 'UTK/USDT', 'XVS/USDT', 'ALPHA/USDT', 'AAVE/USDT', 'NEAR/USDT', 'SXPUP/USDT', 'SXPDOWN/USDT', 'FIL/USDT', 'FILUP/USDT', 'FILDOWN/USDT', 'YFIUP/USDT', 'YFIDOWN/USDT', 'INJ/USDT', 'AUDIO/USDT', 'CTK/USDT', 'BCHUP/USDT', 'BCHDOWN/USDT', 'AKRO/USDT', 'AXS/USDT', 'HARD/USDT', 'DNT/USDT', 'STRAX/USDT', 'UNFI/USDT', 'ROSE/USDT', 'AVA/USDT', 'XEM/USDT', 'AAVEUP/USDT', 'AAVEDOWN/USDT', 'SKL/USDT', 'SUSD/USDT', 'SUSHIUP/USDT', 'SUSHIDOWN/USDT', 'XLMUP/USDT', 'XLMDOWN/USDT', 'GRT/USDT', 'JUV/USDT', 'PSG/USDT', '1INCH/USDT', 'REEF/USDT', 'OG/USDT', 'ATM/USDT', 'ASR/USDT', 'CELO/USDT', 'RIF/USDT', 'BTCST/USDT', 'TRU/USDT', 'CKB/USDT', 'TWT/USDT', 'FIRO/USDT', 'LIT/USDT', 'SFP/USDT', 'DODO/USDT', 'CAKE/USDT', 'ACM/USDT', 'BADGER/USDT', 'FIS/USDT', 'OM/USDT', 'POND/USDT', 'DEGO/USDT', 'ALICE/USDT', 'LINA/USDT', 'PERP/USDT', 'RAMP/USDT', 'SUPER/USDT', 'CFX/USDT', 'EPS/USDT', 'AUTO/USDT', 'TKO/USDT', 'PUNDIX/USDT', 'TLM/USDT', '1INCHUP/USDT', '1INCHDOWN/USDT', 'BTG/USDT', 'MIR/USDT', 'BAR/USDT', 'FORTH/USDT', 'BAKE/USDT', 'BURGER/USDT', 'SLP/USDT', 'SHIB/USDT', 'ICP/USDT', 'AR/USDT', 'POLS/USDT', 'MDX/USDT', 'MASK/USDT', 'LPT/USDT', 'NU/USDT', 'XVG/USDT', 'ATA/USDT', 'GTC/USDT', 'TORN/USDT', 'KEEP/USDT', 'ERN/USDT', 'KLAY/USDT', 'PHA/USDT', 'BOND/USDT', 'MLN/USDT', 'DEXE/USDT', 'C98/USDT', 'CLV/USDT', 'QNT/USDT', 'Fdw/USDT', 'TVK/USDT', 'MINA/USDT', 'RAY/USDT', 'FARM/USDT', 'ALPACA/USDT', 'QUICK/USDT', 'MBOX/USDT', 'FOR/USDT', 'REQ/USDT', 'GHST/USDT', 'WAXP/USDT', 'TRIBE/USDT', 'GNO/USDT', 'XEC/USDT', 'ELF/USDT', 'DYDX/USDT', 'POLY/USDT', 'IDEX/USDT', 'VIDT/USDT', 'USDP/USDT', 'GALA/USDT', 'ILV/USDT', 'YGG/USDT', 'SYS/USDT', 'DF/USDT', 'FIDA/USDT', 'FRONT/USDT', 'CVP/USDT', 'AGLD/USDT', 'RAD/USDT', 'BETA/USDT', 'RARE/USDT', 'LAZIO/USDT', 'CHESS/USDT', 'ADX/USDT', 'AUCTION/USDT', 'DAR/USDT', 'BNX/USDT', 'RGT/USDT', 'MOVR/USDT', 'CITY/USDT', 'ENS/USDT', 'KP3R/USDT', 'QI/USDT', 'PORTO/USDT', 'POWR/USDT', 'VGX/USDT', 'JASMY/USDT', 'AMP/USDT', 'PLA/USDT', 'PYR/USDT', 'RNDR/USDT', 'ALCX/USDT', 'SANTOS/USDT', 'MC/USDT', 'ANY/USDT', 'BICO/USDT', 'FLUX/USDT', 'FXS/USDT', 'VOXEL/USDT', 'up/USDT', 'CVX/USDT', 'PEOPLE/USDT', 'OOKI/USDT', 'SPELL/USDT', 'UST/USDT', 'JOE/USDT', 'ACH/USDT', 'IMX/USDT', 'GLMR/USDT', 'LOKA/USDT', 'SCRT/USDT', 'API3/USDT', 'BTTC/USDT', 'ACA/USDT', 'ANC/USDT', 'XNO/USDT', 'WOO/USDT', 'ALPINE/USDT', 'T/USDT', 'ASTR/USDT', 'NBT/USDT', 'GMT/USDT', 'KDA/USDT']
    #Basic
    bars = binance.fetch_ohlcv(keys[count], timeframe='5m', since=None, limit=200)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] += 32400000
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['keys'] = keys[count]
    #Balance
    balance = binance.fetch_balance()
    current = len(df.index) - 1
    previous = len(df.index) - 2
    try:
        df['maxusdt'] = balance['USDT']['free']
    except:
        df['maxusdt'] = 0
    try:
        df['maxcoin'] = balance[df['keys'][current][:-5]]['free']
    except:
        df['maxcoin'] = 0
    #Run
    data = supertrend(df)
    signals(data)

#Time
try:
    schedule.every(1).minutes.do(run_bot)
    while True:
        schedule.run_pending()
except:
    time.sleep(60)
    schedule.every(1).minutes.do(run_bot)
    while True:
        schedule.run_pending()