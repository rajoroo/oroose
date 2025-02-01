from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData

# ================================= WEEK START =================================
def all_week_data_queryset():
    return StockData.objects.filter(is_wk_fetched=True).order_by("wk_stoch_black_0")


def week_above_50_wma_queryset():
    return StockData.objects.filter(is_wk_fetched=True, wk_ema_50_0__lt=F("wk_close")).order_by("wk_stoch_black_0")


def week_above_50_wma_stoch_cross_queryset():
    return StockData.objects.filter(
        is_wk_fetched=True,
        wk_ema_50_0__lt=F("wk_close"),
        wk_stoch_black_0__gt=F("wk_stoch_red_0"),
        wk_stoch_black_1__lt=F("wk_stoch_red_1"),
    ).order_by("wk_stoch_black_0")


def week_above_50_wma_stoch_positive_queryset():
    return StockData.objects.filter(
        is_wk_fetched=True, wk_ema_50_0__lt=F("wk_close"), wk_stoch_black_0__gt=F("wk_stoch_red_0")
    ).order_by("wk_stoch_black_0")


def week_above_rsi_60_queryset():
    return StockData.objects.filter(
        is_wk_fetched=True, wk_rsi_0__gt=60
    ).order_by("wk_rsi_0")


# ================================= DAY START =================================


def all_day_data_queryset():
    return StockData.objects.filter(is_day_fetched=True).order_by("day_stoch_black_0")


def week_above_50_wma_day_stoch_cross_queryset():
    return StockData.objects.filter(
        is_wk_fetched=True,
        is_day_fetched=True,
        wk_ema_50_0__lt=F("wk_close"),
        day_stoch_black_0__gt=F("day_stoch_red_0"),
        day_stoch_black_1__lt=F("day_stoch_red_1"),
    ).order_by("day_stoch_black_0")


def week_below_50_wma_day_stoch_cross_queryset():
    return StockData.objects.filter(
        is_wk_fetched=True,
        is_day_fetched=True,
        wk_ema_50_0__gt=F("wk_close"),
        day_stoch_black_0__gt=F("day_stoch_red_0"),
        day_stoch_black_1__lt=F("day_stoch_red_1"),
    ).order_by("day_stoch_black_0")


def week_above_50_wma_day_stoch_positive_queryset():
    return StockData.objects.filter(
        is_wk_fetched=True,
        is_day_fetched=True,
        wk_ema_50_0__lt=F("wk_close"),
        day_stoch_black_0__gt=F("day_stoch_red_0"),
    ).order_by("day_stoch_black_0")


def day_cross_50_wma_queryset():
    return StockData.objects.filter(
        is_day_fetched=True,
        wk_ema_50_0__lt=F("wk_close"),
        day_close_0__gt=F("day_ema_50_0"),
        day_close_1__lt=F("day_ema_50_0"),
    ).order_by("day_stoch_black_0")


def day_above_50_wma_queryset():
    return StockData.objects.filter(
        is_day_fetched=True,
        day_ema_50_0__lt=F("day_close"),
    ).order_by("day_stoch_black_0")


def week_level_0_to_20_queryset():
    return (
        StockData.objects.annotate(
            is_wk_stoch_positive=Case(
                When(wk_stoch_black_0__gt=F("wk_stoch_red_0"), then=True),
                default=False,
            ),
            is_day_stoch_positive=Case(
                When(day_stoch_black_0__gt=F("day_stoch_red_0"), then=True),
                default=False,
            ),
        )
        .filter(
            is_wk_fetched=True,
            is_day_fetched=True,
            wk_ema_50_0__lt=F("wk_close"),
            wk_stoch_black_0__lt=20,
            day_stoch_black_0__gt=20,
            is_day_stoch_positive=True,
        )
        .order_by("day_stoch_black_0")
    )


def week_level_20_to_50_queryset():
    return (
        StockData.objects.annotate(
            is_wk_stoch_positive=Case(
                When(wk_stoch_black_0__gt=F("wk_stoch_red_0"), then=True),
                default=False,
            ),
            is_day_stoch_positive=Case(
                When(day_stoch_black_0__gt=F("day_stoch_red_0"), then=True),
                default=False,
            ),
        )
        .filter(
            is_wk_fetched=True,
            is_day_fetched=True,
            wk_ema_50_0__lt=F("wk_close"),
            wk_stoch_black_0__gt=20,
            wk_stoch_black_0__lt=50,
            day_stoch_black_0__gt=20,
            is_day_stoch_positive=True,
        )
        .order_by("day_stoch_black_0")
    )


def week_level_50_to_80_queryset():
    return (
        StockData.objects.filter(
            wk_stoch_black_0__gt=F("wk_stoch_red_0"),
        )
        .annotate(
            is_wk_stoch_cross=Case(
                When(
                    Q(wk_stoch_black_0__gt=F("wk_stoch_red_0")) & Q(wk_stoch_black_1__lt=F("wk_stoch_red_1")),
                    then=True,
                ),
                default=False,
            ),
        )
        .filter(
            is_wk_fetched=True,
            wk_ema_50_0__lt=F("wk_close"),
            wk_stoch_black_0__gt=50,
            wk_stoch_black_0__lt=80,
        )
    )
