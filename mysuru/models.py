from datetime import datetime

from django.db import models

from bengaluru.models import FiveHundred
from core.choice import FhZeroStatus, PlStatus


class FhZeroDownTrend(models.Model):
    date = models.DateField(verbose_name="Date")
    time = models.DateTimeField(verbose_name="Time")
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
    previous_rank = models.IntegerField(verbose_name="Previous Rank", null=True, blank=True)
    previous_price = models.FloatField(verbose_name="Previous Price")
    quantity = models.IntegerField(verbose_name="Quantity")
    last_price = models.FloatField(verbose_name="Last Price")
    buy_price = models.FloatField(verbose_name="Buy Price", default=0.0)
    sell_price = models.FloatField(verbose_name="Sell Price", default=0.0)
    current_price = models.FloatField(verbose_name="Current Price", default=0.0)
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
        super(FhZeroDownTrend, self).save(*args, **kwargs)
