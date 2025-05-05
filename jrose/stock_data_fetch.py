from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData

# ================================= WEEK START =================================
def all_week_data_queryset():
    return StockData.objects.filter(is_wk_fetched=True).order_by("wk_stoch_black_0")


def all_day_data_queryset():
    return StockData.objects.filter(is_day_fetched=True).order_by("day_stoch_black_0")


def all_hr_data_queryset():
    return StockData.objects.filter(is_hr_fetched=True).order_by("hr_stoch_black_0")


def daily_potential_queryset():
    """Daily Potential stocks"""
    return (
        StockData.objects.filter(
            is_day_fetched=True,
            day_ema_200_0__lt=F("day_ema_50_0"),
        )
        .annotate(
            day_stoch_cross_0=Case(
                When(
                    Q(day_stoch_black_0__gt=F("day_stoch_red_0")) & Q(day_stoch_red_1__gt=F("day_stoch_black_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_cross_1=Case(
                When(
                    Q(day_stoch_black_1__gt=F("day_stoch_red_1")) & Q(day_stoch_red_2__gt=F("day_stoch_black_2")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            stoch_cross=Case(
                When(
                    Q(day_stoch_cross_0=True) | Q(day_stoch_cross_1=True),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_ha_cross_0=Case(
                When(
                    Q(day_ha_close_0__gt=F("day_ha_open_0")) &
                    Q(day_ha_open_1__gt=F("day_ha_close_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_ha_cross_1=Case(
                When(
                    Q(day_ha_close_1__gt=F("day_ha_open_1")) &
                    Q(day_ha_open_2__gt=F("day_ha_close_2")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            ha_cross=Case(
                When(
                    Q(day_ha_cross_0=True) | Q(day_ha_cross_1=True),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .order_by("-day_stoch_black_0")
    )
