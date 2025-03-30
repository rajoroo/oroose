from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData

# ================================= WEEK START =================================
def all_week_data_queryset():
    return StockData.objects.filter(is_wk_fetched=True).order_by("wk_stoch_black_0")


def all_day_data_queryset():
    return StockData.objects.filter(is_day_fetched=True).order_by("day_stoch_black_0")


def all_hr_data_queryset():
    return StockData.objects.filter(is_hr_fetched=True).order_by("hr_stoch_black_0")


