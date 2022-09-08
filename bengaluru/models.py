from django.db import models


class FiveHundred(models.Model):
    date = models.DateField(verbose_name="Date")
    time = models.DateTimeField(verbose_name="Time")
    rank = models.IntegerField(verbose_name="Rank")
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isbin = models.CharField(max_length=100, verbose_name="Isbin")
    price = models.FloatField(verbose_name="Price")

    objects = models.Manager()

    class Meta:
        ordering = ["date", "rank"]
