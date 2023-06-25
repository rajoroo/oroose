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

    # return df['rsi'].iloc[-3], df['rsi'].iloc[-2], df['rsi'].iloc[-1]
    return df


def calculate_macd(df):
    k = df["close"].ewm(span=12, adjust=False, min_periods=12).mean()
    d = df["close"].ewm(span=26, adjust=False, min_periods=26).mean()
    macd = k - d
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    macd_h = macd - macd_s
    df["macd"] = df.index.map(macd)
    df["macd_h"] = df.index.map(macd_h)
    df["macd_s"] = df.index.map(macd_s)
    df["macd_crossed"] = np.where(
        (df["macd_s"] > df["macd"]) & (df["macd"].shift(1) > df["macd_s"].shift(1)), "Crossed", np.nan
    )
    df_crossed = df[(df.macd_crossed == "Crossed")]
    macd_limit = df_crossed["macd_h"].iloc[-1] * 1.5
    df["macd_status"] = (df["macd_h"] > macd_limit) & (df["macd_h"] < 0) & (df["macd_crossed"] != "Crossed")
    print(df.tail(10))
    return df


def get_stoch_crossover(df):
    df["ema_200"] = df["close"].ewm(span=200, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_50"] = df["close"].ewm(span=50, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_200_percentage"] = ((df["ema_200"] / df["close"]) - 1) * 100
    df["14-high"] = df["high"].rolling(14).max()
    df["14-low"] = df["low"].rolling(14).min()
    df["k"] = (df["close"] - df["14-low"]) * 100 / (df["14-high"] - df["14-low"])
    df["d"] = df["k"].rolling(3).mean()
    df["k_smooth"] = df["d"].rolling(3).mean()
    df["stoch_crossed"] = np.where(
        (df["d"] > df["k_smooth"]) & (df["k_smooth"].shift(1) > df["d"].shift(1)), "Crossed", np.nan
    )
    df["stoch_status"] = (df["k_smooth"] < 20) & (df["stoch_crossed"] == "Crossed")
    df["stoch_positive_trend"] = df["d"] > df["k_smooth"]
    current_day = df.iloc[-1]

    return {
        "stoch_status": current_day["stoch_status"],
        "date": current_day["date"],
        "ema_200": current_day["ema_200"],
        "ema_50": current_day["ema_50"],
        "ema_200_percentage": current_day["ema_200_percentage"],
        "stoch_positive_trend": current_day["stoch_positive_trend"],
    }


def get_macd_last_two_cross_over(df):
    day_1_status = False
    day_2_status = False

    k = df["close"].ewm(span=12, adjust=False, min_periods=12).mean()
    d = df["close"].ewm(span=26, adjust=False, min_periods=26).mean()
    macd = k - d
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    macd_h = macd - macd_s
    df["macd"] = df.index.map(macd)
    df["macd_h"] = df.index.map(macd_h)
    df["macd_s"] = df.index.map(macd_s)
    df["crossed"] = np.where((df["macd_h"] < 0) & (df["macd_h"].shift(1) > 0), "Crossed", np.nan)
    df["crossed_count"] = df["crossed"].eq("Crossed").cumsum()
    df["ema_200"] = df["close"].ewm(span=200, min_periods=0, adjust=False, ignore_na=False).mean()
    df["ema_50"] = df["close"].ewm(span=50, min_periods=0, adjust=False, ignore_na=False).mean()

    last_crossed_df = df[df["crossed_count"] == df["crossed_count"].max()]
    df = last_crossed_df.reset_index()
    df["ema_200_percentage"] = ((df["ema_200"] / df["close"]) - 1) * 100
    current_day = df.iloc[-1]

    if df.shape[0] > 3:
        day_2 = df.iloc[1]
        day_3 = df.loc[2]

        if current_day["macd_h"] < 0 and current_day["macd_h"] >= day_2["macd_h"]:
            day_1_status = True
        if current_day["macd_h"] < 0 and current_day["macd_h"] >= day_3["macd_h"]:
            day_2_status = True

    return {
        "day_1_status": day_1_status,
        "day_2_status": day_2_status,
        "date": current_day["date"],
        "ema_200": current_day["ema_200"],
        "ema_50": current_day["ema_50"],
        "ema_200_percentage": current_day["ema_200_percentage"],
    }
