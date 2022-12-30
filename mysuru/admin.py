from django.contrib import admin
from mysuru.models import FhZeroDownTrend


@admin.register(FhZeroDownTrend)
class FhZeroDownTrendAdmin(admin.ModelAdmin):
    list_display = ("symbol", "rank", "date", "updated_date", "time", "isin", "last_price")
    date_hierarchy = "date"
