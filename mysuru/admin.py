from django.contrib import admin

from mysuru.models import MacdTrend, StochTrend


@admin.register(MacdTrend)
class MacdAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "updated_date",
        "company_name",
        "price",
        "ema_200",
        "ema_50",
        "day_1_status",
        "day_2_status",
        "trend_status",
    )
    date_hierarchy = "date"


@admin.register(StochTrend)
class StochAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "updated_date",
        "company_name",
        "price",
        "ema_200",
        "ema_50",
        "stoch_status",
        "trend_status",
    )
    date_hierarchy = "date"
