from django.db import models
from django.utils.translation import gettext_lazy as _


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
            models.UniqueConstraint(fields=['date', 'isin'], name='unique_five_hundred')
        ]


class FhZeroStatus(models.TextChoices):
    pass


# class FhZero(models.Model):
#     date = models.DateField(verbose_name="Date")
#     time = models.DateTimeField(verbose_name="Time")
#     tag = models.CharField(max_length=10, verbose_name="Tag")
#     fh_id = models.ForeignKey()
#     symbol = models.CharField(max_length=200, verbose_name="Symbol")
#     isin = models.CharField(max_length=100, verbose_name="Isin")
#     status = ""
#     buy_price = models.FloatField(verbose_name="Buy Price")
#     sell_price = models.FloatField(verbose_name="Sell Price")
#     profit_loss = models.FloatField(verbose_name="Profit Loss")
#
#     objects = models.Manager()


