from datetime import datetime, timedelta

import numpy as np
from django.db import models
import pandas as pd
from core.zero_util import get_history_five_min

from stockwatch.choice import SignalStatus


class StockWatchFh(models.Model):
    date = models.DateField(verbose_name="Date")
    created_date = models.DateTimeField(verbose_name="Created Date")
    stock_data = models.JSONField(verbose_name="Stock Data", null=True, blank=True)
    objects = models.Manager()


class FiveHundred(models.Model):
    date = models.DateField(verbose_name="Date")
    created_date = models.DateTimeField(verbose_name="Created Date")
    rank = models.IntegerField(verbose_name="Rank")
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    last_price = models.FloatField(verbose_name="Price")
    percentage_change = models.FloatField(verbose_name="Percentage")
    signal_status = models.CharField(
        max_length=5,
        choices=SignalStatus.choices,
        default=SignalStatus.INPROG,
    )

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "rank"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_five_hundred")
        ]

    def get_signal_status(self, time_obj):
        signal_status = SignalStatus.INPROG
        # from_date = time_obj - timedelta(hours=1, minutes=40)
        from_date = datetime(2023, 1, 2, 9, 15)
        current_list = get_history_five_min(symbol=self.symbol, from_date=from_date, to_date=time_obj)
        print("*********************************************")
        print(current_list)
        if current_list and len(current_list) > 16:
            df = pd.DataFrame({'close': current_list})
            pre_result, result = self.calculate_rsi(df=df)

            if result < 70 < pre_result:
                signal_status = SignalStatus.SELL
            elif result > 70 > pre_result:
                signal_status = SignalStatus.BUY
            print(pre_result, result, signal_status, self.symbol)
        return signal_status

    def calculate_rsi(self, df):
        df['change'] = df['close'].diff(1)  # Calculate change

        # calculate gain / loss from every change
        df['gain'] = np.select([df['change'] > 0, df['change'].isna()],
                               [df['change'], np.nan],
                               default=0)
        df['loss'] = np.select([df['change'] < 0, df['change'].isna()],
                               [-df['change'], np.nan],
                               default=0)

        # create avg_gain /  avg_loss columns with all nan
        df['avg_gain'] = np.nan
        df['avg_loss'] = np.nan

        n = 14  # what is the window

        # Alternatively
        df['avg_gain'][n] = df.loc[:n, 'gain'].mean()
        df['avg_loss'][n] = df.loc[:n, 'loss'].mean()

        # This is not a pandas way, looping through the pandas series, but it does what you need
        for i in range(n + 1, df.shape[0]):
            df['avg_gain'].iloc[i] = (df['avg_gain'].iloc[i - 1] * (n - 1) + df['gain'].iloc[i]) / n
            df['avg_loss'].iloc[i] = (df['avg_loss'].iloc[i - 1] * (n - 1) + df['loss'].iloc[i]) / n

        # calculate rs and rsi
        df['rs'] = df['avg_gain'] / df['avg_loss']
        df['rsi'] = 100 - (100 / (1 + df['rs']))

        print(df)

        return df['rsi'].iloc[-2], df['rsi'].iloc[-1]
