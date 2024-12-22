from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData


def week_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True
        )
        .annotate(
            wk_stoch_cross=Case(
                When(
                    Q(wk_stoch_black_0__gt=F("wk_stoch_red_0")) &
                    Q(wk_stoch_black_1__lt=F("wk_stoch_red_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .order_by("wk_stoch_black_0")
    )


def day_queryset():
    return (
        StockData.objects.filter(
            is_day_fetched=True
        )
        .annotate(
            day_ha_cross=Case(
                When(
                    Q(day_ha_close_0__gt=F("day_ha_open_0")) &
                    Q(day_ha_open_1__gt=F("day_ha_close_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_cross_0=Case(
                When(
                    Q(day_stoch_black_0__gt=F("day_stoch_red_0")) &
                    Q(day_stoch_black_1__lt=F("day_stoch_red_1")),
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
            day_stoch_cross_20_0=Case(
                When(
                    Q(day_stoch_black_0__gt=20) &
                    Q(day_stoch_black_1__lt=20),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_cross_20_1=Case(
                When(
                    Q(day_stoch_black_1__gt=20) &
                    Q(day_stoch_black_2__lt=20),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_valid=Case(
                When(
                    Q(day_stoch_cross_0=True) |
                    Q(day_stoch_cross_1=True) |
                    Q(day_stoch_cross_20_0=True) |
                    Q(day_stoch_cross_20_1=True),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .order_by("day_stoch_black_0")
    )


def smart_buy_week_stoch_cross_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True
        )
        .annotate(
            wk_stoch_cross=Case(
                When(
                    Q(wk_stoch_black_0__gt=F("wk_stoch_red_0")) &
                    Q(wk_stoch_black_1__lt=F("wk_stoch_red_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .filter(wk_stoch_cross=True)
        .order_by("wk_stoch_black_0")
    )


def smart_buy_day_stoch_cross_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
            is_day_fetched=True,
        )
        .annotate(
            wk_stoch_positive=Case(
                When(
                    wk_stoch_black_0__gt=F("wk_stoch_red_0"),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_cross_0=Case(
                When(
                    Q(day_stoch_black_0__gt=F("day_stoch_red_0")) &
                    Q(day_stoch_black_1__lt=F("day_stoch_red_1")),
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
                    Q(day_stoch_cross_0=True) |
                    Q(day_stoch_cross_1=True),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .filter(
            day_stoch_valid=True,
            wk_stoch_positive=True
        )
        .order_by("day_stoch_black_0")
    )


def smart_buy_day_wma_cross_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
            is_day_fetched=True,
            day_close__gt=F("day_ema_14_0")
        )
        .annotate(
            day_cross_wma=Case(
                When(
                    Q(day_close__gt=F("day_ema_14_0")) &
                    Q(day_open__lt=F("day_ema_14_0")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            )
        )
        .filter(day_cross_wma=True)
        .order_by("day_stoch_black_0")
    )


def smart_buy_day_above_wma_queryset():
    return (
        StockData.objects.filter(
            is_wk_fetched=True,
            is_day_fetched=True,
            day_close__gt=F("day_ema_14_0")
        )
        .order_by("day_stoch_black_0")
    )


