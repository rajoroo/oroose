from django.contrib import admin

from mysuru.models import MacdTrend, StochDailyTrend, StochWeeklyTrend


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


@admin.register(StochDailyTrend)
class StochDailyAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "updated_date",
        "company_name",
        "price",
        "ema_200",
        "ema_50",
        "stoch_status",
        "trend_status",
        "stoch_positive_trend",
        "d_value",
    )
    date_hierarchy = "date"


@admin.register(StochWeeklyTrend)
class StochWeeklyAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "updated_date",
        "company_name",
        "price",
        "ema_200",
        "ema_50",
        "stoch_status",
        "trend_status",
        "stoch_positive_trend",
        "d_value",
    )
    date_hierarchy = "date"
