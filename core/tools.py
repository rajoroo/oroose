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


def calculate_exponential_moving_average(df):
    """Calculate exponential moving average 200, 50 and 20."""
    df["ema_200"] = df["close"].ewm(span=200, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_50"] = df["close"].ewm(span=50, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_20"] = df["close"].ewm(span=20, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_200_percentage"] = ((df["ema_200"] / df["close"]) - 1) * 100
    current = df.iloc[-1]
    return {
        "ema_200": current["ema_200"],
        "ema_50": current["ema_50"],
        "ema_20": current["ema_20"],
        "ema_200_percentage": current["ema_200_percentage"]
    }


def calculate_rsi(df):
    """Calculate RSI dataframe has close price"""
    df["change"] = df["close"].diff(1)  # Calculate change

    # calculate gain / loss from every change
    df["gain"] = np.select([df["change"] > 0, df["change"].isna()], [df["change"], np.nan], default=0)
    df["loss"] = np.select([df["change"] < 0, df["change"].isna()], [-df["change"], np.nan], default=0)

    # create avg_gain /  avg_loss columns with all nan
    df["avg_gain"] = np.nan
    df["avg_loss"] = np.nan

    n = 14  # what is the window

    # Alternatively
    df["avg_gain"][n] = df.loc[:n, "gain"].mean()
    df["avg_loss"][n] = df.loc[:n, "loss"].mean()

    # This is not a pandas way, looping through the pandas series, but it does what you need
    for i in range(n + 1, df.shape[0]):
        df["avg_gain"].iloc[i] = (df["avg_gain"].iloc[i - 1] * (n - 1) + df["gain"].iloc[i]) / n
        df["avg_loss"].iloc[i] = (df["avg_loss"].iloc[i - 1] * (n - 1) + df["loss"].iloc[i]) / n

    # calculate rs and rsi
    df["rs"] = df["avg_gain"] / df["avg_loss"]
    df["rsi"] = 100 - (100 / (1 + df["rs"]))

    current = df.iloc[-1]
    previous = df.iloc[-2]
    return {
        "rsi": current["rsi"],
        "rsi_previous": previous["rsi"],
    }


def calculate_stochastic(df):
    """Calculate Stochastic value"""
    df["14-high"] = df["high"].rolling(14).max()
    df["14-low"] = df["low"].rolling(14).min()
    df["k"] = (df["close"] - df["14-low"]) * 100 / (df["14-high"] - df["14-low"])
    df["d"] = df["k"].rolling(3).mean()
    df["k_smooth"] = df["d"].rolling(3).mean()

    current = df.iloc[-1]
    previous = df.iloc[-2]

    return {
        "stoch_black": current["k_smooth"],
        "stoch_red": current["d"],
        "stoch_black_previous": previous["k_smooth"],
        "stoch_red_previous": previous["d"],
    }


def wma(arr, period):
    kernel = np.arange(period, 0, -1)
    kernel = np.concatenate([np.zeros(period - 1), kernel / kernel.sum()])
    return np.convolve(arr, kernel, "same")


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

    ha_df["wma_20"] = wma(ha_df["close"], 20)

    ha_df["ha_positive"] = np.where(
        ha_df["open"] < ha_df["close"],
        True,
        False,
    )
    ha_df["ha_cross"] = np.where(
        (ha_df["ha_positive"] == True) & (ha_df["ha_positive"].shift(1) == False), True, False
    )

    ha_df["ha_wma_cross"] = np.where(
        (ha_df["open"] < ha_df["wma_20"]) & (ha_df["wma_20"] < ha_df["close"]),
        True,
        False,
    )
    ha_df["ha_wma_top"] = np.where(
        (ha_df["wma_20"] < ha_df["open"]) & (ha_df["wma_20"] < ha_df["close"]) & (ha_df["close"] > ha_df["open"]),
        True,
        False,
    )

    current = ha_df.iloc[-1]
    previous = ha_df.iloc[-2]
    return {
        "ha_open": current["open"],
        "ha_high": current["high"],
        "ha_low": current["low"],
        "ha_close": current["close"],
        "ha_open_previous": previous["open"],
        "ha_high_previous": previous["high"],
        "ha_low_previous": previous["low"],
        "ha_close_previous": previous["close"],
    }


def get_rsi(df, periods=14, ema=True):
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

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return {
        "rsi": np.round(rsi.iloc[-1], decimals=2),
        "rsi_previous": np.round(rsi.iloc[-2], decimals=2),
    }
