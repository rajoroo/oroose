from django.contrib import admin

from mysuru.models import TopTen


@admin.register(TopTen)
class TopTenAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "company_name",
        "last_price",
        "ema_200",
        "ema_50",
        "osc_status",
        "day_status",
        "is_accepted",
    )
    date_hierarchy = "date"
