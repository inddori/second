import pyupbit
import schedule
import telepot
import pandas as pd
import time


UPBIT_Token = "5226076862:AAHslCWGaD3A4Nveq6n7l0cnKqLdD6mmMDg" #UPBTI 텔레그램 봇
me = '1568360717'
UPBIT_bot = telepot.Bot(UPBIT_Token)

def UPBIT_CCI(): #주봉 CCI
    try:
        upbit_ticker = pyupbit.get_tickers(fiat="KRW")
        i = []
        dic = {}
        for upbit in upbit_ticker:
            upbit_df = pyupbit.get_ohlcv(upbit, "week", count=22)
            pd.set_option('display.float_format', lambda x: '%.1f' % x)

            m1_20 = (upbit_df['high']+upbit_df['close']+upbit_df['low'])/3
            m2_20 = m1_20.rolling(20).mean()
            d_20 = m1_20.rolling(20).apply(lambda x: pd.Series(x).mad())
            u_cci_20 = (m1_20-m2_20) / (0.015*d_20)
            cci_20 = u_cci_20[-1]
            thirty = u_cci_20[-2]
            if thirty < cci_20 < -100:
                if upbit == "KRW-BTC" or upbit == "KRW-ETH":
                    pass
                else:
                    rate = (upbit_df['close'][-1] / upbit_df['close'][-2]) - 1
                    if rate < 0:
                        pass
                    elif rate == 0 or rate > 0:
                        two_rate = round(rate, 2)
                        dic[upbit] = two_rate
                        i.append(upbit)
            else:
                pass
            time.sleep(1)

        UPBIT_tickers = list(i)
        UPBIT_tickers.sort()
        amount = len(UPBIT_tickers)
        min_dic = sorted(dic.items(), key = lambda x : x[1])
        if amount > 0:
            UPBIT_bot.sendMessage(me, "주봉 CCI 가상화폐 : " +str(min_dic[0:9]))
        else:
            UPBIT_bot.sendMessage(me, "주봉 CCI 가상화폐는 없습니다")
                
    except Exception as e:
        print(e, upbit)

def MA7():
    try:
        upbit_ticker = pyupbit.get_tickers(fiat="KRW")
        upbit = []
        error = []
        for i in upbit_ticker:
            try:
                ohlc = pyupbit.get_ohlcv(i, interval="week", count = 9)
                pd.set_option('display.float_format', lambda x: '%.1f' % x)
                o = ohlc['open'].rolling(7).mean()
                h = ohlc['high'].rolling(7).mean()
                c = ohlc['close'].rolling(7).mean()
                l= ohlc['low'].rolling(7).mean()
                ohlc4 = (o+h+c+l)/4
                if ohlc4[-1] < ohlc["open"][-1]:
                    close = ohlc["close"][-2]
                    open = ohlc["open"][-2]
                    if close > ohlc4[-2] and open < ohlc4[-2]:
                        upbit.append(i)
                    elif close < ohlc4[-2] and open < ohlc4[-2]:
                        upbit.append(i)
                    else:
                        pass
                time.sleep(1)
            except TypeError as t:
                print(t, i)
                error.append(i)
                time.sleep(1)

        UPBIT_bot.sendMessage(me, "WEEK_7MA 오류 가상화폐 : " +str(error))
        filter_list = set(upbit)
        upbit_tickers = list(filter_list)
        upbit_tickers.sort()
        amount = len(upbit_tickers)
        if amount > 0:
            UPBIT_bot.sendMessage(me, "WEEK_7MA 가상화폐 : " +str(upbit_tickers))
        else:
            UPBIT_bot.sendMessage(me, "WEEK_7MA 가상화폐는 없습니다")

    except Exception as e:
        print(e)
        

def MA60():
    try:
        upbit_ticker = pyupbit.get_tickers(fiat="KRW")
        upbit = []
        error = []
        for i in upbit_ticker:
            try:
                ohlc = pyupbit.get_ohlcv(i, interval="day", count = 62)
                pd.set_option('display.float_format', lambda x: '%.1f' % x)
                o = ohlc['open'].rolling(60).mean()
                h = ohlc['high'].rolling(60).mean()
                c = ohlc['close'].rolling(60).mean()
                l= ohlc['low'].rolling(60).mean()
                ohlc4 = (o+h+c+l)/4
                if ohlc4[-1] < ohlc["open"][-1]: #오늘 시작가가 60일선보다 위인가?
                    close = ohlc["close"][-2]
                    open = ohlc["open"][-2]
                    if close > ohlc4[-2] and open < ohlc4[-2]: #어제 시가는 MA보다 낮지만, 종가는 더 높은가?
                        upbit.append(i)
                    elif close < ohlc4[-2] and open < ohlc4[-2]: #어제 시가와 종가가 MA보다 낮은가?
                        upbit.append(i)
                    else:
                        pass
                time.sleep(1)
            except TypeError as t:
                print(t, i)
                error.append(i)
                time.sleep(1)

        UPBIT_bot.sendMessage(me, "DAY_60MA 오류 가상화폐 : " +str(error))
        filter_list = set(upbit)
        upbit_tickers = list(filter_list)
        upbit_tickers.sort()
        amount = len(upbit_tickers)
        if amount > 0:
            UPBIT_bot.sendMessage(me, "DAY_60MA 가상화폐 : " +str(upbit_tickers))
        else:
            UPBIT_bot.sendMessage(me, "DAY_60MA 가상화폐는 없습니다")

    except Exception as e:
        print(e)
    
schedule.every().monday.at("08:50").do(UPBIT_CCI)
schedule.every().monday.at("08:53").do(MA7)
schedule.every().day.at("08:56").do(MA60)
schedule.every().monday.at("09:03").do(MA7)
schedule.every().day.at("09:01").do(MA60)

while True:
    schedule.run_pending()
    time.sleep(1)