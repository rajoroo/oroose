from django.contrib import admin

from mysuru.models import TopTen, MacdTrend


@admin.register(TopTen)
class TopTenAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "updated_date",
        "company_name",
        "price",
        "ema_200",
        "ema_50",
        "is_valid",
        "trend_status",
    )
    date_hierarchy = "date"


@admin.register(MacdTrend)
class MacdAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "updated_date",
        "company_name",
        "price",
        "ema_200",
        "ema_50",
        "is_valid",
        "trend_status",
    )
    date_hierarchy = "date"
