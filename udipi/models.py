from django.db import models
import numpy as np
from datetime import datetime
from core.zero_util import get_history_day


class StockMaster(models.Model):
    created_date = models.DateField(verbose_name="Created Date")
    updated_date = models.DateField(verbose_name="Updated Date")
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    token = models.CharField(max_length=50, verbose_name="Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    is_processed = models.BooleanField(verbose_name="Is Processed", default=False)
    is_error = models.BooleanField(verbose_name="Is Error", default=False)

    objects = models.Manager()

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return self.symbol

    def calculate_macd(self):
        to_date = datetime.now()
        from_date = datetime(to_date.year - 1, to_date.month, to_date.day - 1)
        df = get_history_day(
            token=self.token,
            from_date=from_date,
            to_date=to_date
        )

        if df is None:
            return None

        k = df['close'].ewm(span=12, adjust=False, min_periods=12).mean()
        d = df['close'].ewm(span=26, adjust=False, min_periods=26).mean()
        macd = k - d
        macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
        macd_h = macd - macd_s
        df['macd'] = df.index.map(macd)
        df['macd_h'] = df.index.map(macd_h)
        df['macd_s'] = df.index.map(macd_s)
        signal = self.generate_signals(df)
        df['buy_signal'] = signal[0]
        df['sell_signal'] = signal[1]

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


class StockMacd(models.Model):
    date = models.DateField(verbose_name="Date")
    stock = models.ForeignKey(
        StockMaster,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Stock",
    )
    open = models.FloatField(verbose_name="Open")
    high = models.FloatField(verbose_name="High")
    low = models.FloatField(verbose_name="Low")
    close = models.FloatField(verbose_name="Close")
    volume = models.FloatField(verbose_name="Volume")
    macd = models.FloatField(verbose_name="MACD")
    macd_histogram = models.FloatField(verbose_name="Histogram")
    macd_signal = models.FloatField(verbose_name="Signal")
    buy_signal = models.FloatField(verbose_name="Buy Signal")
    sell_signal = models.FloatField(verbose_name="Sell Signal")

    objects = models.Manager()
