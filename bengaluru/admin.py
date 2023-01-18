from django.contrib import admin
from bengaluru.models import FhZeroUpTrend


@admin.register(FhZeroUpTrend)
class FhZeroUpTrendAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "rank",
        "date",
        "updated_date",
        "time",
        "isin",
        "last_price",
        "pl_price",
        "error",
        "pl_status"
    )
    date_hierarchy = "date"
