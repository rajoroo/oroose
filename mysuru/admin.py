from django.contrib import admin

from mysuru.models import StockData


@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": [("symbol", "company_name", "smart_token", "smart_token_fetched")]}),
        ("Weekly information", {
            "fields": [
                "is_wk_fetched",
                ("wk_open", "wk_high", "wk_low", "wk_close", "wk_volume"),
                ("wk_ema_200_0", "wk_ema_50_0", "wk_ema_20_0"),
                ("wk_stoch_black_0", "wk_stoch_red_0"),
                ("wk_ha_open_0", "wk_ha_high_0", "wk_ha_low_0", "wk_ha_close_0"),
                ("wk_rsi_0"),
            ],
            "classes": ["collapse"]
        }),
        ("Daily information", {
            "fields": [
                "is_day_fetched",
                ("day_open", "day_high", "day_low", "day_close", "day_volume"),
                ("day_ema_200_0", "day_ema_50_0", "day_ema_20_0"),
                ("day_stoch_black_0", "day_stoch_red_0"),
                ("day_ha_open_0", "day_ha_high_0", "day_ha_low_0", "day_ha_close_0"),
                ("day_rsi_0"),
            ],
            "classes": ["collapse"]
        }),
        ("Hourly information", {
            "fields": [
                "is_hr_fetched",
                ("hr_open", "hr_high", "hr_low", "hr_close", "hr_volume"),
                ("hr_ema_200_0", "hr_ema_50_0", "hr_ema_20_0"),
                ("hr_stoch_black_0", "hr_stoch_red_0"),
                ("hr_ha_open_0", "hr_ha_high_0", "hr_ha_low_0", "hr_ha_close_0"),
                ("hr_rsi_0"),
            ],
            "classes": ["collapse"]
        }),
        ("15 Min information", {
            "fields": [
                "is_m15_fetched",
                ("m15_open", "m15_high", "m15_low", "m15_close", "m15_volume"),
                ("m15_ema_200_0", "m15_ema_50_0", "m15_ema_20_0"),
                ("m15_stoch_black_0", "m15_stoch_red_0"),
                ("m15_ha_open_0", "m15_ha_high_0", "m15_ha_low_0", "m15_ha_close_0"),
                ("m15_rsi_0"),
            ],
            "classes": ["collapse"]
        }),
        ("5 Min information", {
            "fields": [
                "is_m5_fetched",
                ("m5_open", "m5_high", "m5_low", "m5_close", "m5_volume"),
                ("m5_ema_200_0", "m5_ema_50_0", "m5_ema_20_0"),
                ("m5_stoch_black_0", "m5_stoch_red_0"),
                ("m5_ha_open_0", "m5_ha_high_0", "m5_ha_low_0", "m5_ha_close_0"),
                ("m5_rsi_0"),
            ],
            "classes": ["collapse"]
        }),

    ]
