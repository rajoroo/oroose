from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData

# ================================= WEEK START =================================
def all_week_data_queryset():
    return StockData.objects.filter(is_wk_fetched=True).order_by("wk_stoch_black_0")


def all_day_data_queryset():
    return StockData.objects.filter(is_day_fetched=True).order_by("day_stoch_black_0")


def wk_ha_0_cross():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
        )
        .annotate(
            wk_ha_cross_0=Case(
                When(
                    Q(wk_ha_close_0__gt=F("wk_ha_open_0")) &
                    Q(wk_ha_open_1__gt=F("wk_ha_close_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .filter(wk_ha_cross_0=True)
    )


def wk_ha_1_cross():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
        )
        .annotate(
            wk_ha_cross_1=Case(
                When(
                    Q(wk_ha_close_0__gt=F("wk_ha_open_0")) &
                    Q(wk_ha_close_1__gt=F("wk_ha_open_1")) &
                    Q(wk_ha_open_2__gt=F("wk_ha_close_2")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .filter(wk_ha_cross_1=True)
    )


def wk_close_below_ha_0_green_open():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
        )
        .filter(wk_ha_close_0__gt=F("wk_ha_open_0"), wk_close_0__lt=F("wk_ha_open_0"))
    )


def wk_close_below_ha_0_red_open():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
        )
        .filter(wk_ha_close_0__lt=F("wk_ha_open_0"), wk_close_0__lt=F("wk_ha_open_0"))
    )


def wk_close_above_ha_0_red_open():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
        )
        .filter(wk_ha_close_0__lt=F("wk_ha_open_0"), wk_close_0__gt=F("wk_ha_open_0"))
    )
