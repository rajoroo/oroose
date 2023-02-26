from django.contrib import admin

from mysuru.models import TopTen


@admin.register(TopTen)
class TopTenAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "ksec_token",
        "smart_token",
        "date",
        "company_name",
        "isin",
        "last_price",
        "is_valid",
        "ema_200",
        "day_status",
        "is_accepted",
    )
    date_hierarchy = "date"
