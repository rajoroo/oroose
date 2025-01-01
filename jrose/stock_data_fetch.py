from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData

# ================================= WEEK START =================================
def all_week_data_queryset():
    return (
        StockData.objects.filter(is_wk_fetched=True)
        .order_by("wk_stoch_black_0")
    )


def week_above_50_wma_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
            wk_ema_50_0__lt=F("wk_close")
        )
        .order_by("wk_stoch_black_0")
    )


def week_above_50_wma_stoch_cross_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
            wk_ema_50_0__lt=F("wk_close"),
            wk_stoch_black_0__gt=F("wk_stoch_red_0"),
            wk_stoch_black_1__lt=F("wk_stoch_red_1")
        )
        .order_by("wk_stoch_black_0")
    )


def week_above_50_wma_stoch_positive_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
            wk_ema_50_0__lt=F("wk_close"),
            wk_stoch_black_0__gt=F("wk_stoch_red_0")
        )
        .order_by("wk_stoch_black_0")
    )

# ================================= DAY START =================================

def all_day_data_queryset():
    return (
        StockData.objects.filter(is_day_fetched=True)
        .order_by("day_stoch_black_0")
    )


def week_above_50_wma_day_stoch_cross_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
            is_day_fetched=True,
            wk_ema_50_0__lt=F("wk_close"),
            day_stoch_black_0__gt=F("day_stoch_red_0"),
            day_stoch_black_1__lt=F("day_stoch_red_1")
        )
        .order_by("day_stoch_black_0")
    )


def week_above_50_wma_day_stoch_positive_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
            is_day_fetched=True,
            wk_ema_50_0__lt=F("wk_close"),
            day_stoch_black_0__gt=F("day_stoch_red_0")
        )
        .order_by("day_stoch_black_0")
    )

def day_above_50_wma_queryset():
    return (
        StockData.objects.filter(
            is_day_fetched=True,
            day_ema_50_0__lt=F("day_close"),
        )
        .order_by("day_stoch_black_0")
    )
