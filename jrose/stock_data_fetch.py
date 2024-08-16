from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData


def m15_positive_queryset():
    """Short Term 15 Min positive"""
    # Weekly 200 > 50 > 20
    # Daily 200 > 50 > 20
    # 15 Min Stoch cross, EMA cross
    # To cross stoch/EMA and crossed
    return (
        StockData.objects.filter(
            # Weekly
            is_wk_fetched=True,
            wk_ema_200_0__lt=F("wk_ema_50_0"),
            wk_ema_50_0__lt=F("wk_ema_20_0"),
            wk_ema_20_0__lt=F("wk_ha_close_0"),
            wk_ha_open_0__lt=F("wk_ha_close_0"),
            wk_rsi_0__gt=60,
            # Daily
            is_day_fetched=True,
            day_ema_20_0__lt=F("day_ha_close_0"),
            day_ha_open_0__lt=F("day_ha_close_0"),
            day_ha_open_1__lt=F("day_ha_close_1"),
            day_stoch_red_0__lt=F("day_stoch_black_0"),
            # 15 Min
            is_m15_fetched=True,
        )
        .annotate(
            m15_ema_cross_0=Case(
                When(Q(m15_ha_close_0__gt=F("m15_ema_20_0")) & Q(m15_ha_open_0__lt=F("m15_ema_20_0")), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_ema_cross_1=Case(
                When(Q(m15_ha_close_1__gt=F("m15_ema_20_1")) & Q(m15_ha_open_1__lt=F("m15_ema_20_1")), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_ema_cross_2=Case(
                When(Q(m15_ha_close_2__gt=F("m15_ema_20_2")) & Q(m15_ha_open_2__lt=F("m15_ema_20_2")), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_ema_cross_3=Case(
                When(Q(m15_ha_close_3__gt=F("m15_ema_20_3")) & Q(m15_ha_open_3__lt=F("m15_ema_20_3")), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_ema_valid=Case(
                When(m15_ema_cross_0=True, then=Value(True)),
                When(m15_ema_cross_1=True, then=Value(True)),
                When(m15_ema_cross_2=True, then=Value(True)),
                When(m15_ema_cross_3=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_cross_0=Case(
                When(
                    Q(m15_stoch_black_0__gt=F("m15_stoch_red_0")) & Q(m15_stoch_red_1__gt=F("m15_stoch_black_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_cross_1=Case(
                When(
                    Q(m15_stoch_black_1__gt=F("m15_stoch_red_1")) & Q(m15_stoch_red_2__gt=F("m15_stoch_black_2")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_cross_2=Case(
                When(
                    Q(m15_stoch_black_2__gt=F("m15_stoch_red_2")) & Q(m15_stoch_red_3__gt=F("m15_stoch_black_3")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_cross_3=Case(
                When(
                    Q(m15_stoch_black_3__gt=F("m15_stoch_red_3")) & Q(m15_stoch_red_4__gt=F("m15_stoch_black_4")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_valid=Case(
                When(m15_stoch_cross_0=True, then=Value(True)),
                When(m15_stoch_cross_1=True, then=Value(True)),
                When(m15_stoch_cross_2=True, then=Value(True)),
                When(m15_stoch_cross_3=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_full_cross=Case(
                When(Q(m15_ema_20_0__lt=F("m15_ha_open_0")) & Q(m15_ema_20_0__lt=F("m15_ha_close_0")), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_valid=Case(
                When(m15_ema_valid=True, then=Value(True)),
                When(m15_stoch_valid=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )
        .order_by("-m15_full_cross")
    )


def m15_negative_queryset():
    """Short Term 15 Min negative"""
    # Daily Negative
    # 15 Min Stoch cross, EMA cross
    # To cross stoch/EMA and crossed
    return (
        StockData.objects.filter(
            # Daily
            is_day_fetched=True,
            day_ha_open_0__gt=F("day_ha_close_0"),
            day_ha_open_1__gt=F("day_ha_close_1"),
            # 15 Min
            is_m15_fetched=True,
        )
        .annotate(
            m15_ema_cross_0=Case(
                When(Q(m15_ha_close_0__lt=F("m15_ema_20_0")) & Q(m15_ha_open_0__gt=F("m15_ema_20_0")),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_ema_cross_1=Case(
                When(Q(m15_ha_close_1__lt=F("m15_ema_20_1")) & Q(m15_ha_open_1__gt=F("m15_ema_20_1")),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_ema_cross_2=Case(
                When(Q(m15_ha_close_2__lt=F("m15_ema_20_2")) & Q(m15_ha_open_2__gt=F("m15_ema_20_2")),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_ema_cross_3=Case(
                When(Q(m15_ha_close_3__lt=F("m15_ema_20_3")) & Q(m15_ha_open_3__gt=F("m15_ema_20_3")),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_ema_valid=Case(
                When(m15_ema_cross_0=True, then=Value(True)),
                When(m15_ema_cross_1=True, then=Value(True)),
                When(m15_ema_cross_2=True, then=Value(True)),
                When(m15_ema_cross_3=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_cross_0=Case(
                When(
                    Q(m15_stoch_red_0__gt=F("m15_stoch_black_0")) & Q(m15_stoch_black_1__gt=F("m15_stoch_red_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_cross_1=Case(
                When(
                    Q(m15_stoch_red_1__gt=F("m15_stoch_black_1")) & Q(m15_stoch_black_2__gt=F("m15_stoch_red_2")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_cross_2=Case(
                When(
                    Q(m15_stoch_red_2__gt=F("m15_stoch_black_2")) & Q(m15_stoch_black_3__gt=F("m15_stoch_red_3")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_cross_3=Case(
                When(
                    Q(m15_stoch_red_3__gt=F("m15_stoch_black_3")) & Q(m15_stoch_black_4__gt=F("m15_stoch_red_4")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_stoch_valid=Case(
                When(m15_stoch_cross_0=True, then=Value(True)),
                When(m15_stoch_cross_1=True, then=Value(True)),
                When(m15_stoch_cross_2=True, then=Value(True)),
                When(m15_stoch_cross_3=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_valid=Case(
                When(m15_ema_valid=True, then=Value(True)),
                When(m15_stoch_valid=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            m15_full_cross=Case(
                When(Q(m15_ema_20_0__gt=F("m15_ha_open_0")) & Q(m15_ema_20_0__gt=F("m15_ha_close_0")),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .order_by("-m15_full_cross")
    )


def daily_potential_queryset():
    """Daily Potential stocks"""
    return (
        StockData.objects.filter(
            is_day_fetched=True,
            day_ema_200_0__lt=F("day_ema_50_0"),
        )
        .annotate(
            day_50_cross=Case(
                When(Q(day_ema_50_0__gt=F("day_ha_open_0")) & Q(day_ema_50_0__lt=F("day_ha_close_0")), then=Value(True)
                     ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_stoch_cross=Case(
                When(
                    Q(day_stoch_black_0__gt=F("day_stoch_red_0")) & Q(day_stoch_red_1__gt=F("day_stoch_black_1")),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_rsi_cross=Case(
                When(day_rsi_0__gt=60, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            day_valid=Case(
                When(day_50_cross=True, then=Value(True)),
                When(day_stoch_cross=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .filter(day_valid=True)
        .order_by("-day_stoch_black_0")
    )
