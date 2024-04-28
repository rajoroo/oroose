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
        "stoch_black",
        "stoch_red",
        "stoch_black_previous",
        "stoch_red_previous",
        "ha_open",
        "ha_high",
        "ha_low",
        "ha_close",
        "ha_open_previous",
        "ha_high_previous",
        "ha_low_previous",
        "ha_close_previous",
        "rsi",
        "rsi_previous",
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
        "stoch_black",
        "stoch_red",
        "stoch_black_previous",
        "stoch_red_previous",
        "ha_open",
        "ha_high",
        "ha_low",
        "ha_close",
        "ha_open_previous",
        "ha_high_previous",
        "ha_low_previous",
        "ha_close_previous",
        "rsi",
        "rsi_previous",
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
        "stoch_black",
        "stoch_red",
        "stoch_black_previous",
        "stoch_red_previous",
        "ha_open",
        "ha_high",
        "ha_low",
        "ha_close",
        "ha_open_previous",
        "ha_high_previous",
        "ha_low_previous",
        "ha_close_previous",
        "rsi",
        "rsi_previous",
        "is_fetched",
    )
    ordering = ['symbol']
