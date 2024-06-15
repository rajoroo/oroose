from datetime import datetime, time

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db import models

from core.smart_util import SmartInstrument, SmartTool
from core.tools import (
    calculate_stochastic,
    get_param_config_tag,
    calculate_heikin_ashi,
    caculate_rsi,
    calculate_exponential_moving_average,
    get_ema,
    get_stochastic,
    get_heikin_ashi,
    get_rsi,
    get_ohlcv,
)


class StockData(models.Model):
    created_date = models.DateField(verbose_name="Created Date", auto_now_add=True)
    updated_date = models.DateField(verbose_name="Updated Date", auto_now=True)

    symbol = models.CharField(max_length=50, verbose_name="Symbol")
    company_name = models.CharField(max_length=200, verbose_name="Company Name", null=True, blank=True)
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    smart_token_fetched = models.BooleanField(verbose_name="Smart Token Fetched", default=False)

    is_wk_fetched = models.BooleanField(verbose_name="Week Fetched", default=False)
    wk_open = models.FloatField(verbose_name="Open", null=True, blank=True)
    wk_high = models.FloatField(verbose_name="High", null=True, blank=True)
    wk_low = models.FloatField(verbose_name="Low", null=True, blank=True)
    wk_close = models.FloatField(verbose_name="Close", null=True, blank=True)
    wk_volume = models.FloatField(verbose_name="Volume", null=True, blank=True)
    wk_ema_20_0 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_0 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_0 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_0 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_0 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_0 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_0 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_0 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_0 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_rsi_0 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    wk_ema_20_1 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_1 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_1 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_1 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_1 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_1 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_1 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_1 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_1 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_rsi_1 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    wk_ema_20_2 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_2 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_2 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_2 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_2 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_2 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_2 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_2 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_2 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_rsi_2 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    wk_ema_20_3 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_3 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_3 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_3 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_3 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_3 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_3 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_3 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_3 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_rsi_3 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    wk_ema_20_4 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_4 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_4 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_4 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_4 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_4 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_4 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_4 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_4 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_rsi_4 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    wk_ema_20_5 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_5 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_5 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_5 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_5 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_5 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_5 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_5 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_5 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_rsi_5 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    is_day_fetched = models.BooleanField(verbose_name="Day Fetched", default=False)
    day_open = models.FloatField(verbose_name="Open", null=True, blank=True)
    day_high = models.FloatField(verbose_name="High", null=True, blank=True)
    day_low = models.FloatField(verbose_name="Low", null=True, blank=True)
    day_close = models.FloatField(verbose_name="Close", null=True, blank=True)
    day_volume = models.FloatField(verbose_name="Volume", null=True, blank=True)
    day_ema_20_0 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_0 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_0 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_0 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_0 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_0 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_0 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_0 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_0 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_rsi_0 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    day_ema_20_1 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_1 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_1 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_1 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_1 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_1 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_1 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_1 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_1 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_rsi_1 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    day_ema_20_2 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_2 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_2 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_2 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_2 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_2 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_2 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_2 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_2 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_rsi_2 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    day_ema_20_3 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_3 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_3 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_3 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_3 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_3 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_3 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_3 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_3 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_rsi_3 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    day_ema_20_4 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_4 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_4 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_4 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_4 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_4 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_4 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_4 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_4 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_rsi_4 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    day_ema_20_5 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_5 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_5 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_5 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_5 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_5 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_5 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_5 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_5 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_rsi_5 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    is_hr_fetched = models.BooleanField(verbose_name="Hour Fetched", default=False)
    hr_open = models.FloatField(verbose_name="Open", null=True, blank=True)
    hr_high = models.FloatField(verbose_name="High", null=True, blank=True)
    hr_low = models.FloatField(verbose_name="Low", null=True, blank=True)
    hr_close = models.FloatField(verbose_name="Close", null=True, blank=True)
    hr_volume = models.FloatField(verbose_name="Volume", null=True, blank=True)
    hr_ema_20_0 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    hr_ema_50_0 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    hr_ema_200_0 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    hr_stoch_black_0 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    hr_stoch_red_0 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    hr_ha_open_0 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    hr_ha_high_0 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    hr_ha_low_0 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    hr_ha_close_0 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    hr_rsi_0 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    hr_ema_20_1 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    hr_ema_50_1 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    hr_ema_200_1 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    hr_stoch_black_1 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    hr_stoch_red_1 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    hr_ha_open_1 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    hr_ha_high_1 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    hr_ha_low_1 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    hr_ha_close_1 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    hr_rsi_1 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    hr_ema_20_2 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    hr_ema_50_2 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    hr_ema_200_2 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    hr_stoch_black_2 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    hr_stoch_red_2 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    hr_ha_open_2 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    hr_ha_high_2 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    hr_ha_low_2 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    hr_ha_close_2 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    hr_rsi_2 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    hr_ema_20_3 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    hr_ema_50_3 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    hr_ema_200_3 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    hr_stoch_black_3 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    hr_stoch_red_3 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    hr_ha_open_3 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    hr_ha_high_3 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    hr_ha_low_3 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    hr_ha_close_3 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    hr_rsi_3 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    hr_ema_20_4 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    hr_ema_50_4 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    hr_ema_200_4 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    hr_stoch_black_4 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    hr_stoch_red_4 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    hr_ha_open_4 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    hr_ha_high_4 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    hr_ha_low_4 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    hr_ha_close_4 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    hr_rsi_4 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    hr_ema_20_5 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    hr_ema_50_5 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    hr_ema_200_5 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    hr_stoch_black_5 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    hr_stoch_red_5 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    hr_ha_open_5 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    hr_ha_high_5 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    hr_ha_low_5 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    hr_ha_close_5 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    hr_rsi_5 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    is_m15_fetched = models.BooleanField(verbose_name="15 Min Fetched", default=False)
    m15_open = models.FloatField(verbose_name="Open", null=True, blank=True)
    m15_high = models.FloatField(verbose_name="High", null=True, blank=True)
    m15_low = models.FloatField(verbose_name="Low", null=True, blank=True)
    m15_close = models.FloatField(verbose_name="Close", null=True, blank=True)
    m15_volume = models.FloatField(verbose_name="Volume", null=True, blank=True)
    m15_ema_20_0 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m15_ema_50_0 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m15_ema_200_0 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m15_stoch_black_0 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m15_stoch_red_0 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m15_ha_open_0 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m15_ha_high_0 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m15_ha_low_0 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m15_ha_close_0 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m15_rsi_0 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m15_ema_20_1 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m15_ema_50_1 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m15_ema_200_1 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m15_stoch_black_1 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m15_stoch_red_1 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m15_ha_open_1 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m15_ha_high_1 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m15_ha_low_1 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m15_ha_close_1 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m15_rsi_1 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m15_ema_20_2 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m15_ema_50_2 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m15_ema_200_2 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m15_stoch_black_2 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m15_stoch_red_2 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m15_ha_open_2 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m15_ha_high_2 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m15_ha_low_2 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m15_ha_close_2 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m15_rsi_2 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m15_ema_20_3 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m15_ema_50_3 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m15_ema_200_3 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m15_stoch_black_3 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m15_stoch_red_3 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m15_ha_open_3 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m15_ha_high_3 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m15_ha_low_3 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m15_ha_close_3 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m15_rsi_3 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m15_ema_20_4 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m15_ema_50_4 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m15_ema_200_4 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m15_stoch_black_4 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m15_stoch_red_4 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m15_ha_open_4 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m15_ha_high_4 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m15_ha_low_4 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m15_ha_close_4 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m15_rsi_4 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m15_ema_20_5 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m15_ema_50_5 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m15_ema_200_5 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m15_stoch_black_5 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m15_stoch_red_5 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m15_ha_open_5 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m15_ha_high_5 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m15_ha_low_5 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m15_ha_close_5 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m15_rsi_5 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    is_m5_fetched = models.BooleanField(verbose_name="5 Min Fetched", default=False)
    m5_open = models.FloatField(verbose_name="Open", null=True, blank=True)
    m5_high = models.FloatField(verbose_name="High", null=True, blank=True)
    m5_low = models.FloatField(verbose_name="Low", null=True, blank=True)
    m5_close = models.FloatField(verbose_name="Close", null=True, blank=True)
    m5_volume = models.FloatField(verbose_name="Volume", null=True, blank=True)
    m5_ema_20_0 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m5_ema_50_0 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m5_ema_200_0 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m5_stoch_black_0 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m5_stoch_red_0 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m5_ha_open_0 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m5_ha_high_0 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m5_ha_low_0 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m5_ha_close_0 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m5_rsi_0 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m5_ema_20_1 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m5_ema_50_1 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m5_ema_200_1 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m5_stoch_black_1 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m5_stoch_red_1 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m5_ha_open_1 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m5_ha_high_1 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m5_ha_low_1 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m5_ha_close_1 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m5_rsi_1 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m5_ema_20_2 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m5_ema_50_2 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m5_ema_200_2 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m5_stoch_black_2 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m5_stoch_red_2 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m5_ha_open_2 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m5_ha_high_2 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m5_ha_low_2 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m5_ha_close_2 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m5_rsi_2 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m5_ema_20_3 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m5_ema_50_3 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m5_ema_200_3 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m5_stoch_black_3 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m5_stoch_red_3 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m5_ha_open_3 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m5_ha_high_3 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m5_ha_low_3 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m5_ha_close_3 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m5_rsi_3 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m5_ema_20_4 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m5_ema_50_4 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m5_ema_200_4 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m5_stoch_black_4 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m5_stoch_red_4 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m5_ha_open_4 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m5_ha_high_4 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m5_ha_low_4 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m5_ha_close_4 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m5_rsi_4 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    m5_ema_20_5 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    m5_ema_50_5 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    m5_ema_200_5 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    m5_stoch_black_5 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    m5_stoch_red_5 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    m5_ha_open_5 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    m5_ha_high_5 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    m5_ha_low_5 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    m5_ha_close_5 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    m5_rsi_5 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_stock")
        ]

    def __str__(self):
        """String representation of trend"""
        return self.symbol

    def get_smart_token(self):
        """Get smart token from api"""
        try:
            obj = SmartInstrument(instrument=self.symbol)
            result = obj.get_instrument()
            self.smart_token = str(result.get("token"))
        except:
            pass

        self.smart_token_fetched = True
        self.save()

    def get_smart_ohlc(self, interval, days):
        """Get Open, High, Low, Close from smart API"""
        from_date = datetime.now() - relativedelta(days=days)
        tag_data = get_param_config_tag(tag="SMART_HISTORY")
        smart = SmartTool(**tag_data)
        smart.get_object()
        history_data = smart.get_historical_data(
            exchange="NSE",
            symboltoken=self.smart_token,
            interval=interval,
            fromdate=from_date.strftime("%Y-%m-%d %H:%M"),
            todate=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
        logic = {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }

        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        dfw = df.resample("W").apply(logic)
        dfw.index = dfw.index - pd.tseries.frequencies.to_offset("6D")
        dfw.reset_index(inplace=True)
        return dfw

    def get_fetch_params(self, data_type):
        params = {
            "wk": ("ONE_DAY", 900),
            "day": ("ONE_DAY", 400),
            "hr": ("ONE_HOUR", 60),
            "m15": ("FIFTEEN_MINUTE", 60),
            "m5": ("FIVE_MINUTE", 60),
        }
        return params.get(data_type)

    def generate_trend_value(self, data_type):
        """Generate trend value"""
        if not self.smart_token:
            return None

        try:
            interval, days = self.get_fetch_params(data_type)
            df = self.get_smart_ohlc(interval=interval, days=days)
            if data_type == "wk":
                df = self.reset_date_ohlc(df=df)

            df_ohlcv = get_ohlcv(df=df, data_type=data_type)
            df_ema = calculate_exponential_moving_average(df=df)
            df_stoch = calculate_stochastic(df=df)
            df_ha = calculate_heikin_ashi(df=df)
            df_rsi = caculate_rsi(df=df)

            data_ema = get_ema(df_ema, data_type)
            data_stoch = get_stochastic(df_stoch, data_type)
            data_ha = get_heikin_ashi(df_ha, data_type)
            data_rsi = get_rsi(df_rsi, data_type)

            all_data = df_ohlcv | data_ema | data_stoch | data_ha | data_rsi
            for attr, value in all_data.items():
                setattr(self, attr, value)

            setattr(self, f"is_{data_type}_fetched", True)
            self.save()
            print(f"------------------{self.symbol}----------------------")
        except ValueError as ve:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(ve)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        return True


class Trend(models.Model):
    """Common Trend model"""
    created_date = models.DateField(verbose_name="Created Date", auto_now_add=True)
    updated_date = models.DateField(verbose_name="Updated Date", auto_now=True)
    updated_date_1 = models.DateField(verbose_name="Updated Date", auto_now=True)

    symbol = models.CharField(max_length=50, verbose_name="Symbol")
    company_name = models.CharField(max_length=200, verbose_name="Company Name", null=True, blank=True)
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    smart_token_fetched = models.BooleanField(verbose_name="Smart Token Fetched", default=False)

    open = models.FloatField(verbose_name="Open", null=True, blank=True)
    high = models.FloatField(verbose_name="High", null=True, blank=True)
    low = models.FloatField(verbose_name="Low", null=True, blank=True)
    close = models.FloatField(verbose_name="Close", null=True, blank=True)
    volume = models.FloatField(verbose_name="Volume", null=True, blank=True)

    ema_20_0 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    ema_50_0 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    ema_200_0 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    ema_200_percentage_0 = models.FloatField(verbose_name="EMA 200 Percentage", null=True, blank=True)
    stoch_black_0 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    stoch_red_0 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    ha_open_0 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    ha_high_0 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    ha_low_0 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    ha_close_0 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    rsi_0 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    ema_20_1 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    ema_50_1 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    ema_200_1 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    ema_200_percentage_1 = models.FloatField(verbose_name="EMA 200 Percentage", null=True, blank=True)
    stoch_black_1 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    stoch_red_1 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    ha_open_1 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    ha_high_1 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    ha_low_1 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    ha_close_1 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    rsi_1 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    ema_20_2 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    ema_50_2 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    ema_200_2 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    ema_200_percentage_2 = models.FloatField(verbose_name="EMA 200 Percentage", null=True, blank=True)
    stoch_black_2 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    stoch_red_2 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    ha_open_2 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    ha_high_2 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    ha_low_2 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    ha_close_2 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    rsi_2 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    ema_20_3 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    ema_50_3 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    ema_200_3 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    ema_200_percentage_3 = models.FloatField(verbose_name="EMA 200 Percentage", null=True, blank=True)
    stoch_black_3 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    stoch_red_3 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    ha_open_3 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    ha_high_3 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    ha_low_3 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    ha_close_3 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    rsi_3 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    ema_20_4 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    ema_50_4 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    ema_200_4 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    ema_200_percentage_4 = models.FloatField(verbose_name="EMA 200 Percentage", null=True, blank=True)
    stoch_black_4 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    stoch_red_4 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    ha_open_4 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    ha_high_4 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    ha_low_4 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    ha_close_4 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    rsi_4 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    ema_20_5 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    ema_50_5 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    ema_200_5 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    ema_200_percentage_5 = models.FloatField(verbose_name="EMA 200 Percentage", null=True, blank=True)
    stoch_black_5 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    stoch_red_5 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    ha_open_5 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    ha_high_5 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    ha_low_5 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    ha_close_5 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    rsi_5 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    is_fetched = models.BooleanField(verbose_name="Is Fetched", default=False)

    objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_trend")
        ]

    def __str__(self):
        """String representation of trend"""
        return self.symbol

    def get_smart_token(self):
        """Get smart token from api"""
        try:
            obj = SmartInstrument(instrument=self.symbol)
            result = obj.get_instrument()
            self.smart_token = str(result.get("token"))
        except:
            pass

        self.smart_token_fetched = True
        self.save()

    def get_date_range(self):
        """Get date range for trend value"""
        raise NotImplementedError("Date range required for generating trend value.")

    def get_interval(self):
        """Get the interval for smart API"""
        raise NotImplementedError("Interval required for smart API.")

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
        raise NotImplementedError("Reset date to weekly OHLC.")

    def get_smart_ohlc(self):
        """Get Open, High, Low, Close from smart API"""
        from_date, to_date = self.get_date_range()
        tag_data = get_param_config_tag(tag="SMART_HISTORY")
        smart = SmartTool(**tag_data)
        smart.get_object()
        history_data = smart.get_historical_data(
            exchange="NSE",
            symboltoken=self.smart_token,
            interval=self.get_interval(),
            fromdate=from_date.strftime("%Y-%m-%d %H:%M"),
            todate=to_date.strftime("%Y-%m-%d %H:%M"),
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def generate_trend_value(self):
        """Generate trend value"""
        if not self.smart_token:
            return None

        try:
            df = self.get_smart_ohlc()
            df = self.reset_date_ohlc(df=df)
            data = df.iloc[-1]
            self.open = round(data["open"], 2)
            self.high = round(data["high"], 2)
            self.low = round(data["low"], 2)
            self.close = round(data["close"], 2)
            self.volume = round(data["volume"], 2)

            df_ema = calculate_exponential_moving_average(df=df)
            df_stoch = calculate_stochastic(df=df)
            df_ha = calculate_heikin_ashi(df=df)
            df_rsi = caculate_rsi(df=df)

            data_ema = get_ema(df_ema)
            data_stoch = get_stochastic(df_stoch)
            data_ha = get_heikin_ashi(df_ha)
            data_rsi = get_rsi(df_rsi)

            all_data = data_ema | data_stoch | data_ha | data_rsi
            for attr, value in all_data.items():
                setattr(self, attr, value)

            self.is_fetched = True
            self.save()
            print(f"------------------{self.symbol}----------------------")
        except ValueError as ve:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(ve)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return True

    @property
    def ema_200_50(self):
        result = None
        if self.ema_50_0 and self.ema_200_0:
            result = self.ema_50_0 > self.ema_200_0
        return result

    @property
    def ema_50_20(self):
        result = None
        if self.ema_20_0 and self.ema_50_0:
            result = self.ema_20_0 > self.ema_50_0
        return result

    @property
    def ha_green(self):
        result = None
        if self.ha_open_0 and self.close:
            result = self.ha_close_0 > self.ha_open_0
        return result

    @property
    def rsi_60(self):
        result = None
        if self.rsi_0:
            result = self.rsi_0 > 60
        return result

    @property
    def rsi_crossed(self):
        result = None
        if self.rsi_0 and self.rsi_1:
            result = self.rsi_1 < 60 < self.rsi_0
        return result

    @property
    def stoch_positive(self):
        result = None
        if self.stoch_black_0 and self.stoch_red_0:
            result = self.stoch_black_0 > self.stoch_red_0
        return result


class HourlyTrend(Trend):
    """Hourly trend inherits from trend model"""

    class Meta:
        # ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_trend")
        ]

    def get_date_range(self):
        """Get date range for hourly trend"""
        to_date = datetime.now()
        last_month_same_date = to_date - relativedelta(days=60)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_interval(self):
        """Get the interval for smart API"""
        return "ONE_HOUR"

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
        return df


class DailyTrend(Trend):
    """Daily trend inherits from trend model"""
    class Meta:
        # ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_trend")
        ]

    def get_date_range(self):
        """Get date range for daily trend"""
        to_date = datetime.now() - relativedelta(days=1)
        if datetime.now().hour >= 13:
            to_date = datetime.now()

        last_month_same_date = to_date - relativedelta(years=1, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_interval(self):
        """Get the interval for smart API"""
        return "ONE_DAY"

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
        return df


class WeeklyTrend(Trend):
    """Weekly trend inherits from trend model"""
    class Meta:
        # ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_trend")
        ]

    def get_date_range(self):
        """Get date range for weekly trend"""
        to_date = datetime.now() - relativedelta(days=1)
        if datetime.now().hour >= 13:
            to_date = datetime.now()

        last_month_same_date = to_date - relativedelta(years=3, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_interval(self):
        """Get the interval for smart API"""
        return "ONE_HOUR"

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
        logic = {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }

        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        dfw = df.resample("W").apply(logic)
        dfw.index = dfw.index - pd.tseries.frequencies.to_offset("6D")
        dfw.reset_index(inplace=True)
        return dfw
