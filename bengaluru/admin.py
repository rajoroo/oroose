from django.contrib import admin
from bengaluru.models import FhZeroUpTrend


@admin.register(FhZeroUpTrend)
class FhZeroUpTrendAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "rank",
        "date",
        "updated_date",
        "created_date",
        "isin",
        "last_price",
        "pl_price",
        "error",
        "pl_status"
    )
    date_hierarchy = "date"
