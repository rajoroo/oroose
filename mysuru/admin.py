from django.contrib import admin
from mysuru.models import FhZeroDownTrend


@admin.register(FhZeroDownTrend)
class FhZeroDownTrendAdmin(admin.ModelAdmin):
    list_display = ("symbol", "rank", "date", "updated_date", "created_date", "isin", "last_price")
    date_hierarchy = "date"
