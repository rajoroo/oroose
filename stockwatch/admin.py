from django.contrib import admin

from stockwatch.models import FiveHundred, StockWatchFh


@admin.register(FiveHundred)
class FiveHundredAdmin(admin.ModelAdmin):
    list_display = ("symbol", "rank", "date", "created_date", "company_name", "isin", "last_price", "signal_status")
    date_hierarchy = "date"


@admin.register(StockWatchFh)
class StockWatchFhAdmin(admin.ModelAdmin):
    list_display = ("date", "created_date")
    date_hierarchy = "date"
