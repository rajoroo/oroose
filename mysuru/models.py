from datetime import datetime

from django.db import models

from bengaluru.models import FiveHundred
from core.choice import FhZeroStatus, PlStatus


class FhZeroDownTrend(models.Model):
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
    buy_price = models.FloatField(verbose_name="Buy Price", default=0.0)
    sell_price = models.FloatField(verbose_name="Sell Price", default=0.0)
    current_price = models.FloatField(verbose_name="Current Price", default=0.0)
    pl_price = models.FloatField(verbose_name="PL Price", default=0.0)
    error = models.BooleanField(default=False, verbose_name="Error")
    error_message = models.TextField(verbose_name="Error Message", null=True, blank=True)
    pl_status = models.CharField(
        max_length=2,
        choices=PlStatus.choices,
        default=PlStatus.INPROG,
    )

    objects = models.Manager()

    def get_pl_price(self):
        result = 0.0
        if self.sell_price > 0.0 and self.buy_price > 0.0:
            result = self.sell_price - self.buy_price
        elif self.sell_price and self.current_price > 0.0:
            result = self.sell_price - self.current_price

        return self.quantity * result

    class Meta:
        ordering = ["symbol"]

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        self.pl_price = self.get_pl_price()
        super(FhZeroDownTrend, self).save(*args, **kwargs)
