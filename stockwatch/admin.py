from django.contrib import admin
from stockwatch.models import FiveHundred, StockWatchFh


@admin.register(FiveHundred)
class FiveHundredAdmin(admin.ModelAdmin):
    pass


@admin.register(StockWatchFh)
class StockWatchFhAdmin(admin.ModelAdmin):
    pass
