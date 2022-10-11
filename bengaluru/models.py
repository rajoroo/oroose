import secrets
import string
from datetime import datetime
from core.models import ParameterSettings

from django.db import models
from django.conf import settings


FH_RANK_FROM = settings.FH_RANK_FROM  # 1
FH_RANK_TILL = settings.FH_RANK_TILL  # 5
FH_MAX_PRICE = settings.FH_MAX_PRICE  # 4500
FH_MAX_PERCENT = settings.FH_MAX_PERCENT  # 11
FH_MAX_BUY_ORDER = settings.FH_MAX_BUY_ORDER  # 2

FH_ZERO_START = settings.FH_ZERO_START
FH_ZERO_END = settings.FH_ZERO_END
SETTINGS_FH_ZERO = "SETTINGS_FH_ZERO"


class FiveHundred(models.Model):
    date = models.DateField(verbose_name="Date")
    time = models.DateTimeField(verbose_name="Time")
    rank = models.IntegerField(verbose_name="Rank", null=True, blank=True)
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

        if (
            ps.status
            and (FH_RANK_FROM <= self.rank <= FH_RANK_TILL)
            and (1 <= self.last_price <= FH_MAX_PRICE)
            and (self.percentage_change <= FH_MAX_PERCENT)
            and (self.fhzero_set.all().count() <= FH_MAX_BUY_ORDER)
            and (not self.fhzero_set.filter(status__in=["TO_BUY", "PURCHASED", "TO_SELL"]).exists())
            and (start_time <= datetime.now() <= end_time)
            and (datetime.today().weekday() < 5)
        ):
            result = True

        return result

    @property
    def fhz_to_sell_condition(self):
        result = False
        ps = ParameterSettings.objects.get(name=SETTINGS_FH_ZERO)
        if (
            ps.status
            and self.rank > FH_RANK_TILL
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
    tag = models.CharField(max_length=10, verbose_name="Tag")
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
    order_id = models.CharField(max_length=100, verbose_name="Order ID", null=True, blank=True)
    stop_loss_id = models.CharField(max_length=100, verbose_name="Stop Loss ID", null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Quantity")
    last_price = models.FloatField(verbose_name="Last Price")
    buy_price = models.FloatField(verbose_name="Buy Price", default=0.0)
    sell_price = models.FloatField(verbose_name="Sell Price", default=0.0)
    current_price = models.FloatField(verbose_name="Current Price", default=0.0)

    objects = models.Manager()

    class Meta:
        ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(
                fields=["date", "tag"],
                name="%(app_label)s_%(class)s_unique_tag"
            )
        ]

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        if not self.tag:
            tag_list = FhZero.objects.filter(date=datetime.today()).values_list("tag")

            while True:
                alphanum = string.ascii_letters + string.digits
                tag = "".join(secrets.choice(alphanum) for i in range(4))
                if tag not in tag_list:
                    self.tag = tag
                    break

        super(FhZero, self).save(*args, **kwargs)
