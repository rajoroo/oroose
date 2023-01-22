from django.contrib import admin
from udipi.models import StockMaster, StockMacd


@admin.register(StockMaster)
class StockMasterAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "created_date",
        "updated_date",
        "token",
        "identifier",
        "company_name",
        "isin",
    )


@admin.register(StockMacd)
class StockMacdAdmin(admin.ModelAdmin):
    list_display = (
        "stock",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "macd",
        "macd_histogram",
        "macd_signal",
        "buy_signal",
        "sell_signal",
    )
    date_hierarchy = "date"
