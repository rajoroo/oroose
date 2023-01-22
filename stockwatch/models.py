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
        # from_date = datetime.today() - timedelta(days=60)
        from_date = datetime(2022, 1, 20)
        time_obj = datetime(2023, 1, 21)
        df = get_history_day(
            token=self.token,
            open_price=self.open_price,
            from_date=from_date,
            to_date=time_obj
        )
        k = df['close'].ewm(span=12, adjust=False, min_periods=12).mean()
        d = df['close'].ewm(span=26, adjust=False, min_periods=26).mean()
        macd = k - d
        macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
        macd_h = macd - macd_s
        df['macd'] = df.index.map(macd)
        df['macd_h'] = df.index.map(macd_h)
        df['macd_s'] = df.index.map(macd_s)
        signal = self.generate_signals(df)
        df['buy_sig'] = signal[0]
        df['sell_sig'] = signal[1]
        print(df)
        return df

    def generate_signals(self, df):
        buy_list = []
        sell_list = []
        flag = -1

        for i in range(0, len(df)):
            if df['macd'][i] > df['macd_s'][i]:  # first occurence of MACD crossing above signal oine
                sell_list.append(np.nan)  # so first flip above means buy
                if flag != 1:  # after first occurence I record flip to ignore
                    buy_list.append(df['close'][i])  # from here onwards
                    flag = 1
                else:
                    buy_list.append(np.nan)
            elif df['macd'][i] < df['macd_s'][i]:
                buy_list.append(np.nan)
                if flag != 0:
                    sell_list.append(df['close'][i])
                    flag = 0
                else:
                    sell_list.append(np.nan)
            else:
                buy_list.append(np.nan)
                sell_list.append(np.nan)

        return (buy_list, sell_list)
