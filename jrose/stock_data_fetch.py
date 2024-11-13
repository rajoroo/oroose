from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData


def smart_buy_queryset():
    return (
        StockData.objects.filter(
            is_day_fetched=True
        )
        .annotate(
            day_rsi_cross=Case(
                When(Q(day_rsi_0__gt=60) & Q(day_rsi_1__lt=60), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_ha_cross=Case(
                When(
                    Q(day_ha_close_0__gt=F("day_ha_open_0")) &
                    Q(day_ha_open_1__gt=F("day_ha_close_1")) &
                    Q(day_rsi_0__gt=60),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_cross_0=Case(
                When(
                    Q(day_stoch_black_0__gt=F("day_stoch_red_0")) &
                    Q(day_stoch_black_1__lt=F("day_stoch_red_1")) ,
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_cross_1=Case(
                When(
                    Q(day_stoch_black_1__gt=F("day_stoch_red_1")) &
                    Q(day_stoch_black_2__lt=F("day_stoch_red_2")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_valid=Case(
                When(
                    Q(day_stoch_black_0__gt=F("day_stoch_red_0")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .order_by("day_rsi_0")
    )


def hour_queryset():
    return (
        StockData.objects.filter(
            is_hr_fetched=True
        )
        .filter(hr_rsi_0__gt=60)
        .annotate(
            hr_rsi_cross=Case(
                When(Q(hr_rsi_0__gt=60) & Q(hr_rsi_1__lt=60), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .order_by("hr_rsi_0")
    )