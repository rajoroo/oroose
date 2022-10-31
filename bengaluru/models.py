import secrets
import string
from datetime import datetime, timedelta
from django.utils import timezone
from core.models import ParameterSettings

from django.db import models
from django.conf import settings


FH_RANK_FROM = settings.FH_RANK_FROM  # 1
FH_RANK_TILL = settings.FH_RANK_TILL  # 5
FH_GRACE_RANK = settings.FH_GRACE_RANK  # 2
FH_MIN_PRICE = settings.FH_MIN_PRICE  # 20
FH_MAX_PRICE = settings.FH_MAX_PRICE  # 4500
FH_MAX_PERCENT = settings.FH_MAX_PERCENT  # 11
FH_MAX_BUY_ORDER = settings.FH_MAX_BUY_ORDER  # 2

FH_ZERO_START = settings.FH_ZERO_START
FH_ZERO_END = settings.FH_ZERO_END
SETTINGS_FH_ZERO = "SETTINGS_FH_ZERO"


class FiveHundred(models.Model):
    date = models.DateField(verbose_name="Date")
    time = models.DateTimeField(verbose_name="Time")
    rank = models.IntegerField(verbose_name="Rank")
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    last_price = models.FloatField(verbose_name="Price")
    percentage_change = models.FloatField(verbose_name="Percentage")

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "rank"]
        constraints = [
            models.UniqueConstraint(
                fields=["date", "symbol"],
                name="%(app_label)s_%(class)s_unique_five_hundred"
            )
        ]

    @property
    def fhz_to_buy_condition(self):
        result = False

        ps = ParameterSettings.objects.get(name=SETTINGS_FH_ZERO)
        start = datetime.strptime(FH_ZERO_START, '%H%M').time()
        end = datetime.strptime(FH_ZERO_END, '%H%M').time()
        start_time = datetime.combine(datetime.today(), start)
        end_time = datetime.combine(datetime.today(), end)
        before_min = datetime.now() - timedelta(minutes=20)

        if (
            ps.status
            and (FH_RANK_FROM <= self.rank <= FH_RANK_TILL)
            and (FH_MIN_PRICE <= self.last_price <= FH_MAX_PRICE)
            and (self.percentage_change <= FH_MAX_PERCENT)
            and (self.fhzero_set.all().count() <= FH_MAX_BUY_ORDER)
            and (not self.fhzero_set.filter(status__in=["TO_BUY", "PURCHASED", "TO_SELL"]).exists())
            and (start_time <= datetime.now() <= end_time)
            and (datetime.today().weekday() < 5)
        ):
            result = True

        if self.fhzero_set.all():
            latest_fhz = self.fhzero_set.latest('updated_date')
            print(latest_fhz.updated_date, before_min)
            result = True if (latest_fhz.updated_date < before_min) else False

        return result

    @property
    def fhz_to_sell_condition(self):
        result = False
        ps = ParameterSettings.objects.get(name=SETTINGS_FH_ZERO)
        if (
            ps.status
            and self.rank > FH_RANK_TILL + FH_GRACE_RANK
            and self.fhzero_set.filter(status=FhZeroStatus.PURCHASED).exists()
        ):
            result = True

        return result


class FhZeroStatus(models.TextChoices):
    TO_BUY = "TO_BUY", "To Buy"
    PURCHASED = "PURCHASED", "Purchased"
    TO_SELL = "TO_SELL", "To Sell"
    SOLD = "SOLD", "Sold"


class FhZero(models.Model):
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
    stop_loss_id = models.CharField(max_length=100, verbose_name="Stop Loss ID", null=True, blank=True)
    sell_id = models.CharField(max_length=100, verbose_name="Sell ID", null=True, blank=True)

    quantity = models.IntegerField(verbose_name="Quantity")
    last_price = models.FloatField(verbose_name="Last Price")
    buy_price = models.FloatField(verbose_name="Buy Price", default=0.0)
    stop_loss_price = models.FloatField(verbose_name="Buy Price", default=0.0)
    sell_price = models.FloatField(verbose_name="Sell Price", default=0.0)
    current_price = models.FloatField(verbose_name="Current Price", default=0.0)
    error = models.BooleanField(default=False, verbose_name="Error")
    error_message = models.TextField(verbose_name="Error Message", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ["symbol"]

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        super(FhZero, self).save(*args, **kwargs)
