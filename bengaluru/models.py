from datetime import datetime

from django.db import models

from core.choice import FhZeroStatus, PlStatus
from core.ks_util import KsTool
from core.smart_util import SmartTool
from core.tools import get_param_config_tag
from stockwatch.models import FiveHundred


class FhZeroUpTrend(models.Model):
    date = models.DateField(verbose_name="Date")
    created_date = models.DateTimeField(verbose_name="Created Date")
    updated_date = models.DateTimeField(verbose_name="Updated Date", auto_now_add=True)
    five_hundred = models.ForeignKey(
        FiveHundred,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Five Hundred",
    )
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    status = models.CharField(
        max_length=10,
        choices=FhZeroStatus.choices,
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
        super(FhZeroUpTrend, self).save(*args, **kwargs)

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
                self.status = FhZeroStatus.PURCHASED

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
                self.status = FhZeroStatus.SOLD

        elif self.sell_id is None and self.sell_price is None:
            result = obj.generate_order(symbol=self.symbol, quantity=self.quantity, transaction_type="S")
            self.sell_id = result.get("nOrdNo")
            self.error = False if result.get("stat") == "Ok" else True
            self.error_message = result.get("errMsg")

        self.save()

    def maintain_order(self):
        high_price = self.buy_price + (self.buy_price * 0.008)
        buy_price = self.buy_price - (self.buy_price * 0.003)

        tag_data = get_param_config_tag(tag="SMART_TRADE")
        smart = SmartTool(**tag_data)
        smart.get_object()
        ltp_data = smart.get_ltp_data(
            exchange="NSE",
            tradingsymbol=self.symbol,
            symboltoken=self.five_hundred.smart_token
        )
        print(ltp_data, "---LTP", high_price, "-----High", buy_price, "-----BUY")
        if (ltp_data > high_price) or (ltp_data < buy_price):
            self.status = FhZeroStatus.TO_SELL
            self.sell_order()
        if ltp_data > self.high_price:
            self.high_price = ltp_data

        self.current_price = ltp_data
        self.save()

