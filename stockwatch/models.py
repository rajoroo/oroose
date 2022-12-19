from django.db import models
from datetime import datetime, timedelta


class StockWatchFh(models.Model):
    date = models.DateField(verbose_name="Date")
    created_date = models.DateTimeField(verbose_name="Created Date")
    stock_data = models.JSONField(verbose_name="Stock Data", null=True, blank=True)
    objects = models.Manager()


class FiveHundred(models.Model):
    date = models.DateField(verbose_name="Date")
    time = models.DateTimeField(verbose_name="Time")
    created_date = models.DateTimeField(verbose_name="Created Date")
    rank = models.IntegerField(verbose_name="Rank")
    highest_rank = models.IntegerField(verbose_name="Highest Rank", null=True, blank=True)
    lowest_rank = models.IntegerField(verbose_name="Lowest Rank", null=True, blank=True)
    previous_rank = models.IntegerField(verbose_name="Previous Rank", null=True, blank=True)
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    last_price = models.FloatField(verbose_name="Price")
    previous_price = models.FloatField(verbose_name="Previous Price")
    previous_price_20min = models.FloatField(verbose_name="Previous Price 20min", default=0.0)
    percentage_change = models.FloatField(verbose_name="Percentage")

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "rank"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_five_hundred")
        ]

    def get_previous_20_min(self, time_obj):
        stock_watch = 0.0
        before_20_min = time_obj - timedelta(minutes=20)
        before_30_min = time_obj - timedelta(minutes=30)
        obj = StockWatchFh.objects.filter(
            created_date__range=(before_30_min, before_20_min)
        ).order_by("-id").first()

        if (not obj) and (not hasattr(obj, 'stock_data')):
            return stock_watch

        stock_watch = obj.stock_data.get(self.symbol)
        return stock_watch["last_price"]


