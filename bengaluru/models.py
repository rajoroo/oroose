import secrets
import string
from datetime import datetime
from core.configuration import ParameterStore

from django.db import models


FH_RANK_FROM = ParameterStore().get_conf("FH_RANK_FROM")  # 1
FH_RANK_TILL = ParameterStore().get_conf("FH_RANK_TILL")  # 5
FH_MAX_PRICE = ParameterStore().get_conf("FH_MAX_PRICE")  # 4500
FH_MAX_PERCENT = ParameterStore().get_conf("FH_MAX_PERCENT")  # 11
FH_MAX_BUY_ORDER = ParameterStore().get_conf("FH_MAX_BUY_ORDER")  # 2


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
        constraints = [models.UniqueConstraint(fields=["date", "isin"], name="unique_five_hundred")]

    @property
    def fhz_to_buy_condition(self):
        result = False
        if (
            (FH_RANK_FROM <= self.rank <= FH_RANK_TILL)
            and (1 <= self.last_price <= FH_MAX_PRICE)
            and (self.percentage_change <= FH_MAX_PERCENT)
            and (self.fhzero_set.all().count() <= FH_MAX_BUY_ORDER)
            and (not self.fhzero_set.filter(status__in=["TO_BUY", "PURCHASED", "TO_SELL"]).exists())
        ):
            result = True

        return result

    @property
    def fhz_to_sell_condition(self):
        result = False
        purchased_obj = self.fhzero_set.filter(status=FhZeroStatus.PURCHASED)
        if (
            self.rank > FH_RANK_TILL
            and purchased_obj
            and purchased_obj.count() == 1
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
    quantity = models.IntegerField(verbose_name="Quantity")
    last_price = models.FloatField(verbose_name="Last Price")
    buy_price = models.FloatField(null=True, blank=True, verbose_name="Buy Price")
    sell_price = models.FloatField(null=True, blank=True, verbose_name="Sell Price")
    profit_loss = models.FloatField(null=True, blank=True, verbose_name="Profit Loss")

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "symbol"]
        constraints = [models.UniqueConstraint(fields=["date", "tag"], name="%(app_label)s_%(class)s_unique_tag")]

    def save(self, *args, **kwargs):
        tag_list = FhZero.objects.filter(date=datetime.today()).values_list("tag")

        while True:
            alphanum = string.ascii_letters + string.digits
            tag = "".join(secrets.choice(alphanum) for i in range(4))
            if tag not in tag_list:
                self.tag = tag
                break

        super(FhZero, self).save(*args, **kwargs)

