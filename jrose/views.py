from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Case, When, Value, BooleanField
from mysuru.models import StockData
from jrose.stock_data_fetch import m15_positive_queryset, m15_negative_queryset, daily_potential_queryset, \
    strong_buy_stoch_cross_queryset, strong_buy_ha_cross_queryset, buy_queryset, strong_sell_stoch_cross_queryset, \
    smart_buy_queryset, short_by_rsi_cross_queryset


@login_required(login_url="/accounts/login/")
def m15_positive(request):
    """Short Term 15 Min positive"""
    stocks = m15_positive_queryset()
    to_calculate = StockData.objects.filter(
        Q(is_wk_fetched=False) |
        Q(is_day_fetched=False) |
        Q(is_m15_fetched=False)
    ).count()
    total_stock = StockData.objects.filter().all().count()
    m15_crossing = stocks.filter(m15_valid=True)
    m15_crossed = stocks.filter(m15_valid=False)
    stock_list = [
        {
            "title": "15 Min Positive To Cross",
            "stocks": m15_crossing,
            "stock_count": m15_crossing.count(),
            "help": "15 minutes crossing above EMA 20"
        },
        {
            "title": "15 Min Positive",
            "stocks": m15_crossed,
            "stock_count": m15_crossed.count(),
            "help": "15 minutes already crossed above EMA 20"
        }
    ]
    context = {
        "active_page": "trading_monitor",
        "stock_list": stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "trading_monitor/m15_positive_page.html", context)


@login_required(login_url="/accounts/login/")
def m15_negative(request):
    """Short Term 15 Min negative"""
    stocks = m15_negative_queryset()
    to_calculate = StockData.objects.filter(
        Q(is_day_fetched=False) |
        Q(is_m15_fetched=False) |
        Q(is_m5_fetched=False)
    ).count()
    total_stock = StockData.objects.filter().all().count()
    m15_crossing = stocks.filter(m15_valid=True)
    m15_crossed = stocks.filter(m15_valid=False)
    stock_list = [
        {
            "title": "15 Min Negative To Cross",
            "stocks": m15_crossing,
            "stock_count": m15_crossing.count(),
            "help": "15 minutes crossing above EMA 20"
        },
        {
            "title": "15 Min Negative",
            "stocks": m15_crossed,
            "stock_count": m15_crossed.count(),
            "help": "15 minutes already crossed above EMA 20"
        }
    ]
    context = {
        "active_page": "trading_monitor",
        "stock_list": stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "trading_monitor/m15_negative_page.html", context)


@login_required(login_url="/accounts/login/")
def daily_potential(request):
    """Daily potential Stocks"""

    stocks = daily_potential_queryset()
    daily_potential_qs = stocks.filter(
        day_ema_20_0__gt=F("day_ema_50_0"),
        day_ha_close_0__gt=F("day_ema_20_0"),
        day_ha_open_0__gt=F("day_ema_20_0"),
    )
    rsi_stock_qs = StockData.objects.annotate(
        rsi_cross_0=Case(
            When(Q(day_rsi_0__gt=60) & Q(day_rsi_1__lt=60), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
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
        day_rsi_cross=Case(
            When(day_rsi_0__gt=60, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        wk_rsi_cross=Case(
            When(wk_rsi_0__gt=60, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    ).filter(day_rsi_cross=True)
    daily_potential_pk = daily_potential_qs.values_list("pk", flat=True)
    stoch_cross_qs = stocks.filter(~Q(pk__in=daily_potential_pk))
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()
    stock_list = [
        {
            "title": "Daily Potential",
            "stocks": daily_potential_qs,
            "stock_count": daily_potential_qs.count(),
            "help": "Daily Potential stocks"
        },
        {
            "title": "Stoch Cross",
            "stocks": stoch_cross_qs,
            "stock_count": stoch_cross_qs.count(),
            "help": "Stoch Cross Stocks"
        },
        {
            "title": "RSI > 60",
            "stocks": rsi_stock_qs,
            "stock_count": rsi_stock_qs.count(),
            "help": "RSI > 60"

        }
    ]
    context = {
        "active_page": "daily_potential",
        "stock_list": stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/daily_potential.html", context)


@login_required(login_url="/accounts/login/")
def strong_buy_view(request):
    """Strong Buy Stocks"""

    stoch_cross_qs = strong_buy_stoch_cross_queryset()
    ha_cross_qs = strong_buy_ha_cross_queryset()
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "strong_buy",
        "stoch_cross_list": stoch_cross_qs,
        "stoch_cross_count": stoch_cross_qs.count(),
        "ha_cross_list": ha_cross_qs,
        "ha_cross_count": ha_cross_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/strong_buy_page.html", context)


@login_required(login_url="/accounts/login/")
def smart_buy_view(request):
    """Smart Buy Stocks"""

    rsi_cross_qs = smart_buy_queryset().filter(day_rsi_cross=True)
    ha_cross_qs = smart_buy_queryset().filter(day_ha_cross=True)
    day_rsi_above_60_qs = smart_buy_queryset().filter(wk_rsi_0__gt=60)
    m15_positive_qs = smart_buy_queryset().filter(wk_rsi_0__gt=60, m15_positive=True)
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "smart_buy",
        "rsi_cross_list": rsi_cross_qs,
        "rsi_cross_count": rsi_cross_qs.count(),
        "ha_cross_list": ha_cross_qs,
        "ha_cross_count": ha_cross_qs.count(),
        "day_rsi_above_60_list": day_rsi_above_60_qs,
        "day_rsi_above_60_count": day_rsi_above_60_qs.count(),
        "m15_positive_list": m15_positive_qs,
        "m15_positive_count": m15_positive_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/smart_buy_page.html", context)


@login_required(login_url="/accounts/login/")
def buy_view(request):
    """Buy Stocks"""

    stoch_cross_qs = strong_buy_stoch_cross_queryset().values_list("symbol", flat=True)
    ha_cross_qs = strong_buy_ha_cross_queryset().values_list("symbol", flat=True)
    symbols_list = list(stoch_cross_qs) + list(ha_cross_qs)
    stoch_qs = buy_queryset().filter(~Q(symbol__in=symbols_list))
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "buy",
        "stock_list": stoch_qs,
        "stock_count": stoch_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/buy_page.html", context)


@login_required(login_url="/accounts/login/")
def strong_sell_view(request):
    """Strong Sell Stocks"""

    stoch_qs = strong_sell_stoch_cross_queryset()
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "strong_sell",
        "stock_list": stoch_qs,
        "stock_count": stoch_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/strong_sell_page.html", context)


@login_required(login_url="/accounts/login/")
def short_buy_view(request):
    """Short Buy Stocks"""

    rsi_list = short_by_rsi_cross_queryset().filter(m15_rsi_cross=False, m15_rsi_0__gt=60).order_by('?')
    rsi_cross_list = short_by_rsi_cross_queryset().filter(m15_rsi_cross=True, m15_rsi_0__gt=60).order_by('?')
    rsi_cross_above_ema_20 = short_by_rsi_cross_queryset().filter(m15_rsi_cross_above_ema_20=True).order_by('?')
    to_calculate = StockData.objects.filter(
        is_wk_fetched=True,
        is_day_fetched=True,
        is_m15_fetched=False,
        wk_rsi_0__gt=60,
        day_rsi_0__gt=60
    ).count()
    total_stock = StockData.objects.filter(
        is_wk_fetched=True,
        is_day_fetched=True,
        wk_rsi_0__gt=60,
        day_rsi_0__gt=60
    ).all().count()

    context = {
        "active_page": "short_buy",
        "rsi_cross_list": rsi_cross_list,
        "rsi_cross_count": rsi_cross_list.count(),
        "rsi_list": rsi_list,
        "rsi_count": rsi_list.count(),
        "rsi_cross_above_ema_20": rsi_cross_above_ema_20,
        "rsi_cross_above_ema_20_count": rsi_cross_above_ema_20.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/short_buy_page.html", context)
