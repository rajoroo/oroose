import secrets
import string
from datetime import datetime

from django.db import models


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
    def generate_fhz_evaluation(self):
        result = False
        if (
            (1 <= self.rank <= 5)
            and (1 <= self.last_price <= 4500)
            and (self.percentage_change <= 11)
            and (self.fhzero_set.all().count() <= 2)
            and (self.fhzero_set.filter(status__in=["TO_BUY", "PURCHASED", "TO_SELL"]).count() == 0)
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

