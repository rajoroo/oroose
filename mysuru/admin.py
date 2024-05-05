from django.contrib import admin

from mysuru.models import WeeklyTrend, DailyTrend, HourlyTrend


@admin.register(WeeklyTrend)
class WeeklyAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "created_date",
        "updated_date",
        "company_name",
        "smart_token",
        "smart_token_fetched",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "ema_20",
        "ema_50",
        "ema_200",
        "ema_200_percentage",
        "stoch_black_0",
        "stoch_red_0",
        "ha_open_0",
        "ha_high_0",
        "ha_low_0",
        "ha_close_0",
        "rsi_0",
        "is_fetched",
    )
    ordering = ['symbol']


@admin.register(DailyTrend)
class DailyAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "created_date",
        "updated_date",
        "company_name",
        "smart_token",
        "smart_token_fetched",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "ema_20",
        "ema_50",
        "ema_200",
        "ema_200_percentage",
        "stoch_black_0",
        "stoch_red_0",
        "ha_open_0",
        "ha_high_0",
        "ha_low_0",
        "ha_close_0",
        "rsi_0",
        "is_fetched",
    )
    ordering = ['symbol']


@admin.register(HourlyTrend)
class HourlyAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "created_date",
        "updated_date",
        "company_name",
        "smart_token",
        "smart_token_fetched",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "ema_20",
        "ema_50",
        "ema_200",
        "ema_200_percentage",
        "stoch_black_0",
        "stoch_red_0",
        "ha_open_0",
        "ha_high_0",
        "ha_low_0",
        "ha_close_0",
        "rsi_0",
        "is_fetched",
    )
    ordering = ['symbol']
