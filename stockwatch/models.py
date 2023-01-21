from datetime import datetime, timedelta, time

import numpy as np
from django.db import models
import pandas as pd
from core.zero_util import get_history_five_min, get_kite, get_history_day
from core.choice import PlStatus


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
    token = models.CharField(max_length=50, verbose_name="Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    last_price = models.FloatField(verbose_name="Price")
    open_price = models.FloatField(verbose_name="Open Price", null=True, blank=True)
    percentage_change = models.FloatField(verbose_name="Percentage")
    signal_status = models.CharField(
        max_length=5,
        choices=SignalStatus.choices,
        default=SignalStatus.INPROG,
    )
    is_valid = models.BooleanField(default=False, verbose_name="Is Valid")
    pp2 = models.FloatField(verbose_name="PP2", null=True, blank=True)
    pp1 = models.FloatField(verbose_name="PP1", null=True, blank=True)
    pp = models.FloatField(verbose_name="PP0", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "rank"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_five_hundred")
        ]

    def is_valid_stock(self):
        symbol = self.symbol
        kite = get_kite()
        result = False
        instrument = f"NSE:{symbol}"
        quote_response = kite.quote(instrument)

        lower_circuit = quote_response[instrument]["lower_circuit_limit"]
        upper_circuit = quote_response[instrument]["upper_circuit_limit"]

        last_price = quote_response[instrument]["ohlc"]["close"]
        price_lower = last_price - (last_price * 0.09)
        price_upper = last_price + (last_price * 0.09)

        if lower_circuit < price_lower < price_upper < upper_circuit:
            result = True

        self.is_valid = result
        self.save()

    def get_signal_status(self, time_obj):
        signal_status = SignalStatus.INPROG
        today = datetime.today() - timedelta(days=7)
        exact_time = time(hour=9, minute=10)
        from_date = datetime.combine(today, exact_time)

        if (
            self.fhzerodowntrend_set.filter(pl_status=PlStatus.WINNER).exists()
            or self.rank > 9
        ):
            return signal_status

        current_list = get_history_five_min(token=self.token, open_price=self.open_price, from_date=from_date, to_date=time_obj)

        if current_list and len(current_list) > 16:
            df = pd.DataFrame({'close': current_list})
            result_2, result_1, result = self.calculate_rsi(df=df)

            if (result_1 < 70 < result_2) and (result < 70 < result_2):
                signal_status = SignalStatus.SELL
            elif (result_1 > 70 > result_2) and (result > 70 > result_2):
                signal_status = SignalStatus.BUY
            print(result_2, result_1, result, signal_status, self.symbol)
            self.pp2 = result_2
            self.pp1 = result_1
            self.pp = result
            self.save()
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

        return df['rsi'].iloc[-3], df['rsi'].iloc[-2], df['rsi'].iloc[-1]

    def calculate_macd(self, time_obj):
        from_date = datetime.today() - timedelta(days=60)
        current_list = get_history_day(
            token=self.token,
            open_price=self.open_price,
            from_date=from_date,
            to_date=time_obj
        )
        df = pd.DataFrame({'close': current_list})
        df['MA FAST'] = df['close'].ewm(span=12, min_periods=12).mean()
        df['MA SLOW'] = df['close'].ewm(span=26, min_periods=26).mean()
        df['MACD'] = df['MA FAST'] - df['MA SLOW']
        df['Signal'] = df['MACD'].ewm(span=9, min_periods=9).mean()
        df.dropna(inplace=True)
        print(df, "---macd")
        return df
