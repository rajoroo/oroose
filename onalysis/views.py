from mysuru.models import StockData
from core.tools import integrated_tool
import numpy as np

# Create your views here.

def m15_analysis(symbol):
    obj = StockData.objects.get(symbol=symbol)
    df = obj.get_smart_ohlc('FIFTEEN_MINUTE', 60)
    df = integrated_tool(df)
    df['ha_color'] = np.where(df['ha_close'] > df['ha_open'], True, False)
    df['new_date'] = [d.date() for d in df['date']]
    df['new_time'] = [d.time() for d in df['date']]
    df["date_seq"] = df.groupby('new_date').cumcount()
    # df['date_seq'] = df['new_date'].ne(df['new_date'].shift()).cumsum()

    df.ema_200 = df.ema_200.round(2)
    df.ema_50 = df.ema_50.round(2)
    df.ema_20 = df.ema_50.round(2)
    df.red = df.red.round(2)
    df.black = df.black.round(2)
    df.rsi = df.rsi.round(2)

    df['ha_color_1'] = df['ha_color'].shift(-1)
    df['ha_color_2'] = df['ha_color'].shift(-2)
    df["ha_open_1"] = df['ha_open'].shift(-2)
    df['m15_status'] = np.where(
        (df['ha_color'] == True) &
        (df['ha_color_1'] == True) &
        (df['ha_color_2'] == True) &
        (df['date_seq'] == 0)
        , True, False)

    df["ha_cross"] = np.where(
        (df['ha_color'] == True) &
        (df['ha_color'].shift(-1) == False)
        , True, False)
    df = df.drop(columns=['ha_color_1', 'ha_color_2', 'date'])
    df['inc'] = df['ha_color'].ne(df['ha_color'].shift()).cumsum()
    df["inc_seq"] = df.groupby('inc').cumcount()

    dfc = df.groupby('new_date')['inc']
    df['l_min'] = dfc.transform('min')
    df = df.drop(df[df.inc != df.l_min].index)


    dfc = df.groupby('new_date')['inc_seq']
    df['m_min'] = dfc.transform('min')
    df['m_max'] = dfc.transform('max')

    df["m_val"] = np.where(
        (df['m_min'] == df['inc_seq']) |
        (df['m_max'] == df['inc_seq'])
        , True, False)

    df = df.drop(df[df.m_val == False].index)
    df = df.reset_index(drop=True)
    df['ha_close_1'] = df['ha_close'].shift(-1)
    df = df[['new_date', 'm15_status', 'rsi', 'ha_open_1', 'ha_close_1']]
    df["percentage"] = ((df["ha_close_1"] - df["ha_open_1"]) / df["ha_open_1"]) * 100
    df = df.drop(df[df.m15_status == False].index)
    # df = df.drop(df[df.rsi < 60].index)
    result = df.loc[:, 'percentage'].mean()
    # print(result)

    print(df)

    return result

def m15_get_percentage():
    recs = StockData.objects.all()

    data = {}

    for rec in recs:
        val = m15_analysis(rec.symbol)
        print(rec.symbol, "---", val)
        print("---------------------------------------------")
        data[rec.symbol] = val

    print(data)
    return data


def hr_analysis(symbol):
    obj = StockData.objects.get(symbol=symbol)
    df = obj.get_smart_ohlc('ONE_HOUR', 60)
    df = integrated_tool(df)
    df['stoch_cross_pos'] = np.where((df['black'] > df['red']) & (df['black'].shift(1) < df['red'].shift(1)), True, False)
    df['stoch_cross_neg'] = np.where((df['black'] < df['red']) & (df['black'].shift(1) > df['red'].shift(1)), True, False)
    df['stoch_cross'] = np.where(df['stoch_cross_pos'] | df['stoch_cross_neg'], True, False)
    df = df.drop(df[df.stoch_cross == False].index)
    df = df.reset_index(drop=True)
    df["next_close"] = df['close'].shift(-1)
    df = df.drop(df[df.stoch_cross_neg == False].index)
    df = df.reset_index(drop=True)
    df["percentage"] = ((df["next_close"] - df["close"]) / df["close"]) * 100
    # print(df)
    result = df.loc[:, 'percentage'].mean()
    # print(result)
    return result


def hr_get_percentage():
    recs = StockData.objects.all()

    data = {}

    for rec in recs:
        val = hr_analysis(rec.symbol)
        print(rec.symbol, "---", val)
        print("---------------------------------------------")
        data[rec.symbol] = val

    print(data)
    return data

def wma(arr, period):
    kernel = np.arange(period, 0, -1)
    kernel = np.concatenate([np.zeros(period - 1), kernel / kernel.sum()])
    return np.convolve(arr, kernel, 'same')


def m5_analysis(symbol):
    obj = StockData.objects.get(symbol=symbol)
    df = obj.get_smart_ohlc('FIVE_MINUTE', 90)
    df = integrated_tool(df)
    df['ha_ema_5'] = wma(df['ha_close'], 5)
    df['ha_ema_50'] = wma(df['ha_close'], 50)
    df["pv"] = df["ha_ema_5"] >= df["ha_ema_50"]
    df["nv"] = df["ha_ema_5"] <= df["ha_ema_50"]
    diff = df['ha_ema_5'] < df['ha_ema_50']
    diff_forward = diff.shift(1)
    crossing = np.where(abs(diff - diff_forward) == 1)[0]
    df = df.iloc[crossing]
    df = df[["date", "ha_close", "ha_ema_5", "ha_ema_50", "pv", "nv"]]
    df["next_close"] = df['ha_close'].shift(-1)
    df["percentage"] = ((df["next_close"] - df["ha_close"]) / df["ha_close"]) * 100
    df = df.drop(df[df.nv == False].index)
    result = df.loc[:, 'percentage'].mean()
    print(result)
    return df


def m5_get_percentage():
    recs = StockData.objects.all()

    data = {}

    for rec in recs:
        val = m5_analysis(rec.symbol)
        print(rec.symbol, "---", val)
        print("---------------------------------------------")
        data[rec.symbol] = val

    print(data)
    return data


def day_analysis(symbol):
    obj = StockData.objects.get(symbol=symbol)
    df = obj.get_smart_ohlc('ONE_DAY', 400)
    df = integrated_tool(df)
    df['ha_ema_5'] = wma(df['ha_close'], 5)
    df['ha_ema_20'] = wma(df['ha_close'], 20)
    df["pv"] = df["ha_ema_5"] >= df["ha_ema_20"]
    df["nv"] = df["ha_ema_5"] <= df["ha_ema_20"]
    diff = df['ha_ema_5'] < df['ha_ema_20']
    diff_forward = diff.shift(1)
    crossing = np.where(abs(diff - diff_forward) == 1)[0]
    df = df.iloc[crossing]
    df = df[["date", "ha_close", "ha_ema_5", "ha_ema_20", "pv", "nv"]]
    df["next_close"] = df['ha_close'].shift(-1)
    df["percentage"] = ((df["next_close"] - df["ha_close"]) / df["ha_close"]) * 100
    df = df.drop(df[df.nv == False].index)
    result = df.loc[:, 'percentage'].mean()
    print(result)
    return df

def day_get_percentage():
    recs = StockData.objects.all()

    data = {}

    for rec in recs:
        val = day_analysis(rec.symbol)
        print(rec.symbol, "---", val)
        print("---------------------------------------------")
        data[rec.symbol] = val

    print(data)
    return data