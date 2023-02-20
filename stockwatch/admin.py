from django.contrib import admin

from stockwatch.models import FiveHundred, StockWatchFh


@admin.register(FiveHundred)
class FiveHundredAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "ksec_token",
        "smart_token",
        "rank",
        "date",
        "created_date",
        "company_name",
        "isin",
        "open_price",
        "last_price",
        "signal_status",
        "is_valid",
        "pp2",
        "pp1",
        "pp",
        "pp2_price",
        "pp1_price",
        "pp_price",
    )
    date_hierarchy = "date"


@admin.register(StockWatchFh)
class StockWatchFhAdmin(admin.ModelAdmin):
    list_display = ("date", "created_date")
    date_hierarchy = "date"
