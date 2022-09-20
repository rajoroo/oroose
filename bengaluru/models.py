from django.db import models
import string
import secrets
from datetime import datetime


class FiveHundred(models.Model):
    date = models.DateField(verbose_name="Date")
    time = models.DateTimeField(verbose_name="Time")
    sequence = models.CharField(max_length=4, verbose_name="Sequence")
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
            models.UniqueConstraint(fields=['date', 'isin'], name='unique_five_hundred')
        ]

    def save(self, *args, **kwargs):
        objs = FiveHundred.objects.filter(date=datetime.today()).values_list("sequence")
        print(objs)
        # alphanum = string.ascii_letters + string.digits
        # self.sequence = ''.join(secrets.choice(alphanum) for i in range(4))
        super(FiveHundred, self).save(*args, **kwargs)


class FhZeroStatus(models.TextChoices):
    TO_BUY = "TO_BUY", "To Buy"
    PURCHASED = "PURCHASED", "Purchased"
    TO_SELL = "TO_SELL", "To Sell"
    SOLD = "SOLD", "Sold"


class FhZero(models.Model):
    date = models.DateField(verbose_name="Date")
    time = models.DateTimeField(verbose_name="Time")
    tag = models.CharField(max_length=10, verbose_name="Tag")
    fh_id = models.ForeignKey(
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
    buy_price = models.FloatField(verbose_name="Buy Price")
    sell_price = models.FloatField(verbose_name="Sell Price")
    profit_loss = models.FloatField(verbose_name="Profit Loss")

    objects = models.Manager()


