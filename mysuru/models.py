from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from core.ks_util import KsecInstrument
from core.smart_util import SmartInstrument, SmartTool
from core.tools import calculate_macd, get_param_config_tag, get_today_datetime
from stockwatch.stocks import PriceBand
import pandas as pd
from core.ks_util import KsTool


class DayStatus(models.TextChoices):
    YES = "YES", _("Yes")
    NO = "NO", _("No")


class TrendStatus(models.TextChoices):
    TO_BUY = "TO_BUY", "To Buy"
    PURCHASED = "PURCHASED", "Purchased"
    TO_SELL = "TO_SELL", "To Sell"
    SOLD = "SOLD", "Sold"


class PlStatus(models.TextChoices):
    WINNER = "WR", _("Winner")
    RUNNER = "RR", _("Runner")
    INPROG = "IP", _("In-Progress")


class TopTen(models.Model):
    date = models.DateField(verbose_name="Date")
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    ksec_token = models.CharField(max_length=50, verbose_name="Ksec Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    last_price = models.FloatField(verbose_name="Price")
    percentage_change = models.FloatField(verbose_name="Percentage")
    is_valid = models.BooleanField(default=False, verbose_name="Is Valid")
    is_accepted = models.BooleanField(default=False, verbose_name="Is Accepted")
    ema_200 = models.FloatField(verbose_name="Ema200", null=True, blank=True)
    last_close = models.FloatField(verbose_name="Last Close", null=True, blank=True)
    day_macd = models.FloatField(verbose_name="MACD", null=True, blank=True)
    day_macd_signal = models.FloatField(verbose_name="MACD Signal", null=True, blank=True)
    day_macd_histogram = models.FloatField(verbose_name="MACD Histogram", null=True, blank=True)
    day_status = models.CharField(
        max_length=5,
        choices=DayStatus.choices,
        default=DayStatus.NO,
    )
    macd = models.FloatField(verbose_name="MACD", null=True, blank=True)
    macd_signal = models.FloatField(verbose_name="MACD Signal", null=True, blank=True)
    macd_histogram = models.FloatField(verbose_name="MACD Histogram", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "symbol"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_top_ten")
        ]

    def get_year_date_difference(self):
        now = datetime.now()
        if now.hour < 18:
            now = datetime.now() - relativedelta(days=1)

        to_date = now
        last_month_same_date = to_date - relativedelta(years=1, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_month_date_difference(self):
        now = datetime.now()
        if now.hour < 18:
            now = datetime.now() - relativedelta(days=1)

        to_date = now
        last_month_same_date = to_date - relativedelta(months=1, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_date_difference(self):
        to_date = datetime.now()
        last_month_same_date = to_date - relativedelta(months=1, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_smart_token(self):
        try:
            obj = SmartInstrument(instrument=self.symbol)
            result = obj.get_instrument()
            self.smart_token = str(result.get("token"))
        except:
            pass
        self.save()

    def get_ksec_token(self):
        obj = KsecInstrument(instrument=self.symbol)
        result = obj.get_instrument()
        self.ksec_token = str(result.get("pSymbol"))
        self.save()

    def is_valid_stock(self):
        band = PriceBand(instrument=self.symbol)
        if self.smart_token and band.get_valid_instrument():
            self.is_valid = True
            self.save()

    def get_day_status(self):
        config = get_param_config_tag(tag="MYSURU")
        if (
                self.is_valid
                and self.last_price
                and self.ema_200
                and self.day_macd
                and self.day_macd_signal
                and self.macd
                and self.macd_signal
                and (self.last_price > config["min_price"])
                and (self.last_price < config["max_price"])
                and (self.percentage_change < config["max_percentage"])
                and (self.last_price > self.ema_200)
                and (self.day_macd > self.day_macd_signal)
                and (self.macd_signal > self.macd)
        ):
            self.day_status = DayStatus.YES
        else:
            self.day_status = DayStatus.NO

        self.save()

    def get_year_macd(self):
        from_date, to_date = self.get_year_date_difference()

        data = self.generate_macd(
            interval="ONE_DAY",
            from_date=from_date,
            to_date=to_date
        )
        self.day_macd = data[0]
        self.day_macd_signal = data[1]
        self.day_macd_histogram = data[2]
        self.save()

    def get_day_macd(self):
        if not((self.last_price > self.ema_200) and (self.day_macd > self.day_macd_signal)):
            return False

        from_date, to_date = self.get_month_date_difference()
        data = self.generate_macd(
            interval="FIVE_MINUTE",
            from_date=from_date,
            to_date=to_date
        )
        self.macd = data[0]
        self.macd_signal = data[1]
        self.macd_histogram = data[2]
        self.save()

    def get_macd(self):
        from_date, to_date = self.get_date_difference()
        data = self.generate_macd(
            interval="FIVE_MINUTE",
            from_date=from_date,
            to_date=to_date
        )
        self.macd = data[0]
        self.macd_signal = data[1]
        self.macd_histogram = data[2]
        self.save()

    def generate_macd(self, interval, from_date, to_date):
        tag_data = get_param_config_tag(tag="SMART_TRADE")
        smart = SmartTool(**tag_data)
        smart.get_object()
        history_data = smart.get_historical_data(
            exchange="NSE",
            symboltoken=self.smart_token,
            interval=interval,
            fromdate=from_date.strftime("%Y-%m-%d %H:%M"),
            todate=to_date.strftime("%Y-%m-%d %H:%M")
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)

        current_list = df["close"].to_list()

        if current_list and len(current_list) > 16:
            df = pd.DataFrame({'close': current_list})
            result_df = calculate_macd(df=df)

            macd = round(result_df['macd'].iloc[-1], 2)
            macd_signal = round(result_df['macd_s'].iloc[-1], 2)
            macd_histogram = round(result_df['macd_h'].iloc[-1], 2)
            return macd, macd_signal, macd_histogram
        return None, None, None

    def get_basic_requirement(self):
        requirement = False

        config = get_param_config_tag(tag="MYSURU")
        start_time = get_today_datetime(time_str=config.get("start_time"))
        end_time = get_today_datetime(time_str=config.get("end_time"))
        trend_status = [TrendStatus.TO_BUY, TrendStatus.PURCHASED, TrendStatus.TO_SELL]
        pl_status = [PlStatus.WINNER, PlStatus.INPROG]

        if (
            config.get("mysuru_status")
            and self.is_valid is True
            and self.day_status == DayStatus.YES
            and (self.mysurutrend_set.all().count() < config["max_buy_order"])
            and (not self.mysurutrend_set.filter(status__in=trend_status).exists())
            and (not self.mysurutrend_set.filter(pl_status__in=pl_status).exists())
            and (not self.mysurutrend_set.filter(error=True).exists())
            and (start_time <= datetime.now() <= end_time)
            and (datetime.today().weekday() < 5)
        ):
            requirement = True

        return requirement

    def get_pre_order_requirement(self):
        requirement = True
        before_20_min = datetime.now() - timedelta(minutes=20)

        if self.mysurutrend_set.all():
            latest_fhz = self.mysurutrend_set.latest("updated_date")
            if latest_fhz.updated_date > before_20_min:
                requirement = False

        return requirement

    def get_standard_requirement(self):
        requirement = False

        # Return False is the condition didn't pass basic and pre-order requirement
        if not (self.get_basic_requirement() and self.get_pre_order_requirement()):
            return False

        if self.macd > self.macd_signal:
            requirement = True

        return requirement


class MysuruTrend(models.Model):
    date = models.DateField(verbose_name="Date")
    created_date = models.DateTimeField(verbose_name="Created Date")
    updated_date = models.DateTimeField(verbose_name="Updated Date", auto_now_add=True)
    top_ten = models.ForeignKey(
        TopTen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Top Ten",
    )
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    status = models.CharField(
        max_length=10,
        choices=TrendStatus.choices,
        verbose_name="Status",
    )
    buy_id = models.CharField(max_length=100, verbose_name="Buy ID", null=True, blank=True)
    sell_id = models.CharField(max_length=100, verbose_name="Sell ID", null=True, blank=True)
    rank = models.IntegerField(verbose_name="Rank")
    quantity = models.IntegerField(verbose_name="Quantity")
    last_price = models.FloatField(verbose_name="Last Price")
    buy_price = models.FloatField(verbose_name="Buy Price", null=True, blank=True)
    sell_price = models.FloatField(verbose_name="Sell Price", null=True, blank=True)
    current_price = models.FloatField(verbose_name="Current Price", null=True, blank=True)
    high_price = models.FloatField(verbose_name="Current Price", null=True, blank=True)
    pl_price = models.FloatField(verbose_name="PL Price", null=True, blank=True)
    error = models.BooleanField(default=False, verbose_name="Error")
    error_message = models.TextField(verbose_name="Error Message", null=True, blank=True)
    pl_status = models.CharField(
        max_length=2,
        choices=PlStatus.choices,
        default=PlStatus.INPROG,
    )

    objects = models.Manager()

    class Meta:
        ordering = ["symbol"]

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        self.pl_price = self.get_pl_price()
        super(MysuruTrend, self).save(*args, **kwargs)

    def get_pl_price(self):
        result = 0.0
        print(self.buy_price, self.sell_price, self.current_price)
        if self.sell_price and self.sell_price > 0.0 and self.buy_price and self.buy_price > 0.0:
            result = self.sell_price - self.buy_price
        elif self.buy_price and self.current_price and self.current_price > 0.0:
            result = self.current_price - self.buy_price
        return self.quantity * result

    def get_ks_session(self):
        config = get_param_config_tag(tag="KSEC")
        return KsTool(**config)

    def buy_order(self):
        obj = self.get_ks_session()

        if self.buy_id is not None and self.buy_price is None:
            result = obj.get_order_book(order_no=self.buy_id)
            price = float(result.get("avgPrc"))
            self.buy_price = price
            self.high_price = price
            self.current_price = price
            self.error = False if result.get("ordSt") == "complete" else True
            self.error_message = result.get("rejRsn")
            if result.get("ordSt") == "complete":
                self.pl_status = PlStatus.INPROG
                self.status = TrendStatus.PURCHASED

        elif self.buy_id is None and self.buy_price is None:
            result = obj.generate_order(symbol=self.symbol, quantity=self.quantity, transaction_type="B")
            self.buy_id = result.get("nOrdNo")
            self.error = False if result.get("stat") == "Ok" else True
            self.error_message = result.get("errMsg")

        self.save()

    def sell_order(self):
        obj = self.get_ks_session()

        if self.sell_id is not None and self.sell_price is None:
            result = obj.get_order_book(order_no=self.sell_id)
            self.sell_price = float(result.get("avgPrc"))
            self.error = False if result.get("ordSt") == "complete" else True
            self.error_message = result.get("rejRsn")
            if result.get("ordSt") == "complete":
                self.pl_status = PlStatus.RUNNER
                self.status = TrendStatus.SOLD

        elif self.sell_id is None and self.sell_price is None:
            result = obj.generate_order(symbol=self.symbol, quantity=self.quantity, transaction_type="S")
            self.sell_id = result.get("nOrdNo")
            self.error = False if result.get("stat") == "Ok" else True
            self.error_message = result.get("errMsg")

        self.save()

    def maintain_order(self):
        high_price = self.high_price - (self.high_price * 0.003)
        buy_price = self.buy_price - (self.buy_price * 0.003)

        tag_data = get_param_config_tag(tag="SMART_TRADE")
        smart = SmartTool(**tag_data)
        smart.get_object()
        ltp_data = smart.get_ltp_data(
            exchange="NSE",
            tradingsymbol=self.symbol,
            symboltoken=self.top_ten.smart_token
        )
        print(ltp_data,"---LTP", high_price, "-----High", buy_price, "-----BUY")
        if (ltp_data < high_price) or (ltp_data < buy_price):
            self.status = TrendStatus.TO_SELL
            self.sell_order()
        if ltp_data > self.high_price:
            self.high_price = ltp_data

        self.current_price = ltp_data
        self.save()
