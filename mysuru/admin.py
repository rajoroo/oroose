from django.contrib import admin

from mysuru.models import TopTen


@admin.register(TopTen)
class TopTenAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "updated_date",
        "company_name",
        "last_price",
        "ema_200",
        "ema_50",
        "osc_status",
        "day_status",
    )
    date_hierarchy = "date"
