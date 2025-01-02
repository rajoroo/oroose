import csv
import io
from datetime import datetime

import numpy as np
import pandas as pd

from core.models import ParameterConfig


def get_param_config_tag(tag):
    """Get all param configs related to the tag"""
    recs = ParameterConfig.objects.filter(tag=tag)
    if not recs:
        return None

    return {rec.name: rec.content for rec in recs}


def save_param_config_tag(params, tag):
    for key, value in params.items():
        rec = ParameterConfig.objects.get(name=key, tag=tag)
        attr = f"content_{rec.config_type.lower()}"
        setattr(rec, attr, value)
        rec.save()

    return True


def check_valid_configs(row, config_type):
    """Todo: add other types"""
    content = row["content"]

    if row["config_type"].lower() == config_type:
        if config_type in ["char", "text", "bool", "date"] and not pd.isnull(content):
            return content
        elif config_type in ["int"] and not pd.isnull(content):
            return int(content)
        elif config_type in ["float"] and not pd.isnull(content):
            return float(content)

    return None


def get_today_datetime(time_str):
    """
    Get today's time
    Ex:
        today = 2020-08-26
        time_str = 1020
        output is datetime.datetime(2020, 8, 26, 10, 20)
    """
    time_val = datetime.strptime(time_str, "%H%M").time()
    time_obj = datetime.combine(datetime.today(), time_val)
    return time_obj


def handle_config_file(csv_file):
    csv_data = io.StringIO(csv_file.read().decode("utf-8"))
    df = pd.read_json(csv_data)
    df = pd.json_normalize(df["data"])
    df = df.dropna(subset=["nick_name"])
    df["length"] = df["content"].astype(str).map(len)
    ParameterConfig.objects.all().delete()

    configs = [
        ParameterConfig(
            date=datetime.now(),
            sequence=row["sequence"],
            name=row["name"],
            nick_name=row["nick_name"],
            config_type=row["config_type"].upper(),
            tag=row["tag"],
            description=row["description"],
            comment=row["comment"],
            content_bool=check_valid_configs(row, "bool"),
            content_char=check_valid_configs(row, "char"),
            content_text=check_valid_configs(row, "text"),
            content_float=check_valid_configs(row, "float"),
            content_int=check_valid_configs(row, "int"),
            content_date=check_valid_configs(row, "date"),
        )
        for index, row in df.iterrows()
    ]
    ParameterConfig.objects.bulk_create(configs)


# def wma(arr, period):
#     kernel = np.arange(period, 0, -1)
#     kernel = np.concatenate([np.zeros(period - 1), kernel / kernel.sum()])
#     return np.convolve(arr, kernel, 'same')


def wma(df, column="close", n=20):

    weights = np.arange(1, n + 1)
    wmas = df[column].rolling(n).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True).to_list()

    return wmas


def calculate_exponential_moving_average(df):
    """Calculate exponential moving average 200, 50 and 20."""
    df["ema_200"] = df["close"].ewm(span=200, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_50"] = df["close"].ewm(span=50, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_20"] = df["close"].ewm(span=20, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_14"] = df["close"].ewm(span=14, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_5"] = df["close"].ewm(span=5, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_200_percentage"] = ((df["ema_200"] / df["close"]) - 1) * 100
    return df


def calculate_weighted_moving_average(df):
    """Calculate exponential moving average 200, 50 and 20."""
    df["ema_200"] = wma(df, "close", 200)
    df["ema_50"] = wma(df, "close", 50)
    df["ema_20"] = wma(df, "close", 20)
    df["ema_14"] = wma(df, "close", 14)
    df["ema_5"] = wma(df, "close", 5)
    df["ema_200_percentage"] = ((df["ema_200"] / df["close"]) - 1) * 100
    return df


def calculate_stochastic(df):
    """Calculate Stochastic value"""
    df["14-high"] = df["high"].rolling(14).max()
    df["14-low"] = df["low"].rolling(14).min()
    df["k"] = (df["close"] - df["14-low"]) * 100 / (df["14-high"] - df["14-low"])
    df["d"] = df["k"].rolling(3).mean()
    df["k_smooth"] = df["d"].rolling(3).mean()
    return df


def calculate_heikin_ashi(df):
    """Calculate Heikin-Ashi candle sticks"""
    ha_df = pd.DataFrame(index=df.index.values, columns=["open", "high", "low", "close"])
    ha_df["close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4

    for i in range(len(df)):
        if i == 0:
            ha_df.iat[0, 0] = df["open"].iloc[0]
        else:
            ha_df.iat[i, 0] = (ha_df.iat[i - 1, 0] + ha_df.iat[i - 1, 3]) / 2

    ha_df["high"] = ha_df.loc[:, ["open", "close"]].join(df["high"]).max(axis=1)
    ha_df["low"] = ha_df.loc[:, ["open", "close"]].join(df["low"]).min(axis=1)
    return ha_df


def caculate_rsi(df, periods=14, ema=True):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df["close"].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema == True:
        # Use exponential moving average
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    df_rsi = ma_up / ma_down
    df_rsi = 100 - (100 / (1 + df_rsi))
    # return {
    #     "rsi": np.round(rsi.iloc[-1], decimals=2),
    # }
    return df_rsi


def get_ohlcv(df, data_type):
    if len(df.index) > 7:
        return {
            f"{data_type}_open": round(df.iloc[-1]["open"], 2),
            f"{data_type}_close": round(df.iloc[-1]["close"], 2),
            f"{data_type}_close_0": round(df.iloc[-1]["close"], 2),
            f"{data_type}_close_1": round(df.iloc[-2]["close"], 2),
            f"{data_type}_close_2": round(df.iloc[-3]["close"], 2),
            f"{data_type}_close_3": round(df.iloc[-4]["close"], 2),
            f"{data_type}_close_4": round(df.iloc[-5]["close"], 2),
            f"{data_type}_close_5": round(df.iloc[-6]["close"], 2),
            f"{data_type}_high": round(df.iloc[-1]["high"], 2),
            f"{data_type}_low": round(df.iloc[-1]["low"], 2),
            f"{data_type}_volume": round(df.iloc[-1]["volume"], 2),
        }

    return {
        f"{data_type}_open": 0,
        f"{data_type}_close": 0,
        f"{data_type}_high": 0,
        f"{data_type}_low": 0,
        f"{data_type}_volume": 0,
    }


def get_ema(df, data_type):
    current = df.iloc[-1]
    if len(df.index) > 7:
        return {
            f"{data_type}_ema_200_0": round(df.iloc[-1]["ema_200"], 2),
            f"{data_type}_ema_50_0": round(df.iloc[-1]["ema_50"], 2),
            f"{data_type}_ema_20_0": round(df.iloc[-1]["ema_20"], 2),
            f"{data_type}_ema_14_0": round(df.iloc[-1]["ema_14"], 2),
            f"{data_type}_ema_5_0": round(df.iloc[-1]["ema_5"], 2),
            f"{data_type}_ema_200_1": round(df.iloc[-2]["ema_200"], 2),
            f"{data_type}_ema_50_1": round(df.iloc[-2]["ema_50"], 2),
            f"{data_type}_ema_20_1": round(df.iloc[-2]["ema_20"], 2),
            f"{data_type}_ema_14_1": round(df.iloc[-1]["ema_14"], 2),
            f"{data_type}_ema_5_1": round(df.iloc[-2]["ema_5"], 2),
            f"{data_type}_ema_200_2": round(df.iloc[-3]["ema_200"], 2),
            f"{data_type}_ema_50_2": round(df.iloc[-3]["ema_50"], 2),
            f"{data_type}_ema_20_2": round(df.iloc[-3]["ema_20"], 2),
            f"{data_type}_ema_14_2": round(df.iloc[-1]["ema_14"], 2),
            f"{data_type}_ema_5_2": round(df.iloc[-3]["ema_5"], 2),
            f"{data_type}_ema_200_3": round(df.iloc[-4]["ema_200"], 2),
            f"{data_type}_ema_50_3": round(df.iloc[-4]["ema_50"], 2),
            f"{data_type}_ema_20_3": round(df.iloc[-4]["ema_20"], 2),
            f"{data_type}_ema_14_3": round(df.iloc[-1]["ema_14"], 2),
            f"{data_type}_ema_5_3": round(df.iloc[-4]["ema_5"], 2),
            f"{data_type}_ema_200_4": round(df.iloc[-5]["ema_200"], 2),
            f"{data_type}_ema_50_4": round(df.iloc[-5]["ema_50"], 2),
            f"{data_type}_ema_20_4": round(df.iloc[-5]["ema_20"], 2),
            f"{data_type}_ema_14_4": round(df.iloc[-1]["ema_14"], 2),
            f"{data_type}_ema_5_4": round(df.iloc[-5]["ema_5"], 2),
            f"{data_type}_ema_200_5": round(df.iloc[-6]["ema_200"], 2),
            f"{data_type}_ema_50_5": round(df.iloc[-6]["ema_50"], 2),
            f"{data_type}_ema_20_5": round(df.iloc[-6]["ema_20"], 2),
            f"{data_type}_ema_14_5": round(df.iloc[-1]["ema_14"], 2),
            f"{data_type}_ema_5_5": round(df.iloc[-6]["ema_5"], 2),
        }
    return {
        f"{data_type}_ema_200_0": 0,
        f"{data_type}_ema_50_0": 0,
        f"{data_type}_ema_20_0": 0,
        f"{data_type}_ema_14_0": 0,
        f"{data_type}_ema_5_0": 0,
        f"{data_type}_ema_200_1": 0,
        f"{data_type}_ema_50_1": 0,
        f"{data_type}_ema_20_1": 0,
        f"{data_type}_ema_14_1": 0,
        f"{data_type}_ema_5_1": 0,
        f"{data_type}_ema_200_2": 0,
        f"{data_type}_ema_50_2": 0,
        f"{data_type}_ema_20_2": 0,
        f"{data_type}_ema_14_2": 0,
        f"{data_type}_ema_5_2": 0,
        f"{data_type}_ema_200_3": 0,
        f"{data_type}_ema_50_3": 0,
        f"{data_type}_ema_20_3": 0,
        f"{data_type}_ema_14_3": 0,
        f"{data_type}_ema_5_3": 0,
        f"{data_type}_ema_200_4": 0,
        f"{data_type}_ema_50_4": 0,
        f"{data_type}_ema_20_4": 0,
        f"{data_type}_ema_14_4": 0,
        f"{data_type}_ema_5_4": 0,
        f"{data_type}_ema_200_5": 0,
        f"{data_type}_ema_50_5": 0,
        f"{data_type}_ema_20_5": 0,
        f"{data_type}_ema_14_5": 0,
        f"{data_type}_ema_5_5": 0,
    }


def get_stochastic(df, data_type):
    if len(df.index) > 7:
        return {
            f"{data_type}_stoch_black_0": round(df.iloc[-1]["d"], 2),
            f"{data_type}_stoch_black_1": round(df.iloc[-2]["d"], 2),
            f"{data_type}_stoch_black_2": round(df.iloc[-3]["d"], 2),
            f"{data_type}_stoch_black_3": round(df.iloc[-4]["d"], 2),
            f"{data_type}_stoch_black_4": round(df.iloc[-5]["d"], 2),
            f"{data_type}_stoch_black_5": round(df.iloc[-6]["d"], 2),
            f"{data_type}_stoch_red_0": round(df.iloc[-1]["k_smooth"], 2),
            f"{data_type}_stoch_red_1": round(df.iloc[-2]["k_smooth"], 2),
            f"{data_type}_stoch_red_2": round(df.iloc[-3]["k_smooth"], 2),
            f"{data_type}_stoch_red_3": round(df.iloc[-4]["k_smooth"], 2),
            f"{data_type}_stoch_red_4": round(df.iloc[-5]["k_smooth"], 2),
            f"{data_type}_stoch_red_5": round(df.iloc[-6]["k_smooth"], 2),
        }
    return {
        f"{data_type}_stoch_black_0": 0,
        f"{data_type}_stoch_black_1": 0,
        f"{data_type}_stoch_black_2": 0,
        f"{data_type}_stoch_black_3": 0,
        f"{data_type}_stoch_black_4": 0,
        f"{data_type}_stoch_black_5": 0,
        f"{data_type}_stoch_red_0": 0,
        f"{data_type}_stoch_red_1": 0,
        f"{data_type}_stoch_red_2": 0,
        f"{data_type}_stoch_red_3": 0,
        f"{data_type}_stoch_red_4": 0,
        f"{data_type}_stoch_red_5": 0,
    }


def get_heikin_ashi(df, data_type):
    if len(df.index) > 7:
        return {
            f"{data_type}_ha_open_0": round(df.iloc[-1]["open"], 2),
            f"{data_type}_ha_high_0": round(df.iloc[-1]["high"], 2),
            f"{data_type}_ha_low_0": round(df.iloc[-1]["low"], 2),
            f"{data_type}_ha_close_0": round(df.iloc[-1]["close"], 2),
            f"{data_type}_ha_open_1": round(df.iloc[-2]["open"], 2),
            f"{data_type}_ha_high_1": round(df.iloc[-2]["high"], 2),
            f"{data_type}_ha_low_1": round(df.iloc[-2]["low"], 2),
            f"{data_type}_ha_close_1": round(df.iloc[-2]["close"], 2),
            f"{data_type}_ha_open_2": round(df.iloc[-3]["open"], 2),
            f"{data_type}_ha_high_2": round(df.iloc[-3]["high"], 2),
            f"{data_type}_ha_low_2": round(df.iloc[-3]["low"], 2),
            f"{data_type}_ha_close_2": round(df.iloc[-3]["close"], 2),
            f"{data_type}_ha_open_3": round(df.iloc[-4]["open"], 2),
            f"{data_type}_ha_high_3": round(df.iloc[-4]["high"], 2),
            f"{data_type}_ha_low_3": round(df.iloc[-4]["low"], 2),
            f"{data_type}_ha_close_3": round(df.iloc[-4]["close"], 2),
            f"{data_type}_ha_open_4": round(df.iloc[-5]["open"], 2),
            f"{data_type}_ha_high_4": round(df.iloc[-5]["high"], 2),
            f"{data_type}_ha_low_4": round(df.iloc[-5]["low"], 2),
            f"{data_type}_ha_close_4": round(df.iloc[-5]["close"], 2),
            f"{data_type}_ha_open_5": round(df.iloc[-6]["open"], 2),
            f"{data_type}_ha_high_5": round(df.iloc[-6]["high"], 2),
            f"{data_type}_ha_low_5": round(df.iloc[-6]["low"], 2),
            f"{data_type}_ha_close_5": round(df.iloc[-6]["close"], 2),
        }

    return {
        f"{data_type}_ha_open_0": 0,
        f"{data_type}_ha_high_0": 0,
        f"{data_type}_ha_low_0": 0,
        f"{data_type}_ha_close_0": 0,
        f"{data_type}_ha_open_1": 0,
        f"{data_type}_ha_high_1": 0,
        f"{data_type}_ha_low_1": 0,
        f"{data_type}_ha_close_1": 0,
        f"{data_type}_ha_open_2": 0,
        f"{data_type}_ha_high_2": 0,
        f"{data_type}_ha_low_2": 0,
        f"{data_type}_ha_close_2": 0,
        f"{data_type}_ha_open_3": 0,
        f"{data_type}_ha_high_3": 0,
        f"{data_type}_ha_low_3": 0,
        f"{data_type}_ha_close_3": 0,
        f"{data_type}_ha_open_4": 0,
        f"{data_type}_ha_high_4": 0,
        f"{data_type}_ha_low_4": 0,
        f"{data_type}_ha_close_4": 0,
        f"{data_type}_ha_open_5": 0,
        f"{data_type}_ha_high_5": 0,
        f"{data_type}_ha_low_5": 0,
        f"{data_type}_ha_close_5": 0,
    }


def get_rsi(df, data_type):
    if len(df.index) > 7:
        return {
            f"{data_type}_rsi_0": round(df.iloc[-1], 2),
            f"{data_type}_rsi_1": round(df.iloc[-2], 2),
            f"{data_type}_rsi_2": round(df.iloc[-3], 2),
            f"{data_type}_rsi_3": round(df.iloc[-4], 2),
            f"{data_type}_rsi_4": round(df.iloc[-5], 2),
            f"{data_type}_rsi_5": round(df.iloc[-6], 2),
        }
    return {
        f"{data_type}_rsi_0": 0,
        f"{data_type}_rsi_1": 0,
        f"{data_type}_rsi_2": 0,
        f"{data_type}_rsi_3": 0,
        f"{data_type}_rsi_4": 0,
        f"{data_type}_rsi_5": 0,
    }


def integrated_tool(df):
    df_expo = calculate_exponential_moving_average(df)
    df_expo_1 = df_expo[["ema_200", "ema_50", "ema_20", "ema_5"]]
    df_stoch = calculate_stochastic(df)
    df_stoch = df_stoch[["k_smooth", "d"]]
    df_stoch = df_stoch.rename(columns={"k_smooth": "red", "d": "black"})
    df_stoch_1 = df_stoch[["red", "black"]]
    df_ha = calculate_heikin_ashi(df)
    df_ha = df_ha[["open", "high", "low", "close"]]
    df_ha = df_ha.rename(columns={"open": "ha_open", "high": "ha_high", "low": "ha_low", "close": "ha_close"})
    df_ha_1 = df_ha[["ha_open", "ha_close"]]
    df_rsi = caculate_rsi(df)
    df_rsi.name = "rsi"

    df_new = df[["date", "open", "high", "low", "close"]]
    df_list = [df_new, df_expo_1, df_stoch_1, df_ha_1, df_rsi]
    result = pd.concat(df_list, axis=1)
    return result
