from django.contrib import admin

from mysuru.models import TopTen


@admin.register(TopTen)
class TopTenAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "company_name",
        "last_price",
        "is_valid",
        "ema_200",
        "ema_50",
        "osc_status",
        "macd_status",
        "day_status",
        "is_accepted",
    )
    date_hierarchy = "date"
