from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import F, Q, Case, When, Value, BooleanField

from mysuru.forms import TradingForm
from mysuru.fetch_trend import FetchTrend
from mysuru.models import StockData
from datetime import datetime
from mysuru.task import trading_m5_fetch
from django_q.tasks import schedule
from django_q.models import Schedule
import arrow


# =========================================Fiters=========================================
potential_stock_filters = {
    "is_wk_fetched": True,
    "wk_ema_200_1__lt": F("wk_ema_20_1"),
    "wk_ema_50_1__lt": F("wk_ema_20_1"),
    "wk_ha_open_1__lt": F("wk_ha_close_1"),
    "wk_ema_20_1__lt": F("wk_ha_open_1"),
    "wk_ha_open_2__lt": F("wk_ha_open_1"),
    "wk_ha_close_2__lt": F("wk_ha_close_1"),
    "wk_rsi_1__gt": 60,
}
potential_negative_stock_filters = {
    "is_wk_fetched": True,
    "wk_ha_open_1__gt": F("wk_ha_close_1"),
}
# =========================================Trend==========================================
@login_required(login_url="/accounts/login/")
def stock_data_week_page(request):
    """Trend page for display Weekly"""
    total_stock = StockData.objects.all().count()
    all_stock_list = StockData.objects.all()
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    context = {
        "title": "Weekly",
        "stocks": all_stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "active_page": "stock_data",
    }
    return render(request, "stock/weekly_page.html", context)


@login_required(login_url="/accounts/login/")
def stock_data_day_page(request):
    """Trend page for display Daily"""
    total_stock = StockData.objects.all().count()
    all_stock_list = StockData.objects.all()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    context = {
        "title": "Daily",
        "stocks": all_stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "active_page": "stock_data",
    }
    return render(request, "stock/daily_page.html", context)


@login_required(login_url="/accounts/login/")
def stock_data_hour_page(request):
    """Trend page for display Hourly"""
    total_stock = StockData.objects.all().count()
    all_stock_list = StockData.objects.all()
    to_calculate = StockData.objects.filter(is_hr_fetched=False).count()
    context = {
        "title": "Hourly",
        "stocks": all_stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "active_page": "stock_data",
    }
    return render(request, "stock/hourly_page.html", context)


@login_required(login_url="/accounts/login/")
def stock_data_15min_page(request):
    """Trend page for display 15 Min"""
    total_stock = StockData.objects.all().count()
    all_stock_list = StockData.objects.all()
    to_calculate = StockData.objects.filter(is_m15_fetched=False).count()
    context = {
        "title": "15 Min",
        "stocks": all_stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "active_page": "stock_data",
    }
    return render(request, "stock/m15_page.html", context)


@login_required(login_url="/accounts/login/")
def stock_data_5min_page(request):
    """Trend page for display 15 Min"""
    total_stock = StockData.objects.all().count()
    all_stock_list = StockData.objects.all()
    to_calculate = StockData.objects.filter(is_m5_fetched=False).count()
    context = {
        "title": "15 Min",
        "stocks": all_stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "active_page": "stock_data",
    }
    return render(request, "stock/m5_page.html", context)


@login_required(login_url="/accounts/login/")
def potential_page(request):
    """Trend page for display potential"""
    total_stock = StockData.objects.all().count()
    if datetime.today().weekday() > 4:
        filter_params = {
            "is_wk_fetched": True,
            "wk_ema_200_0__lt": F("wk_ema_20_0"),
            "wk_ema_50_0__lt": F("wk_ema_20_0"),
            "wk_ha_open_0__lt": F("wk_ha_close_0"),
            "wk_ema_20_0__lt": F("wk_ha_open_0"),
            "wk_ha_open_1__lt": F("wk_ha_open_0"),
            "wk_ha_close_1__lt": F("wk_ha_close_0"),
            "wk_rsi_0__gt": 60,
        }
        annotate_params = {
            "ha_cross_0": Case(
                When(
                    Q(wk_ha_open_0__lt=F("wk_ha_close_0")) & Q(wk_ha_open_1__gt=F("wk_ha_close_1")), then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            "rsi_cross_0": Case(
                When(Q(wk_rsi_0__gt=60) & Q(wk_rsi_1__lt=60), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        }
    else:
        filter_params = {
            "is_wk_fetched": True,
            "wk_ema_200_1__lt": F("wk_ema_20_1"),
            "wk_ema_50_1__lt": F("wk_ema_20_1"),
            "wk_ha_open_1__lt": F("wk_ha_close_1"),
            "wk_ema_20_1__lt": F("wk_ha_open_1"),
            "wk_ha_open_2__lt": F("wk_ha_open_1"),
            "wk_ha_close_2__lt": F("wk_ha_close_1"),
            "wk_rsi_1__gt": 60,
        }
        annotate_params = {
            "ha_cross_1": Case(
                When(
                    Q(wk_ha_open_1__lt=F("wk_ha_close_1")) & Q(wk_ha_open_2__gt=F("wk_ha_close_2")), then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            "rsi_cross_1": Case(
                When(Q(wk_rsi_1__gt=60) & Q(wk_rsi_2__lt=60), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        }
    potential_stock_list = StockData.objects.filter(**filter_params).annotate(**annotate_params)
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    record_type = True if datetime.today().weekday() > 4 else False
    context = {
        "title": "Potential Stocks",
        "stocks": potential_stock_list,
        "record_type": record_type,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "potential_count": potential_stock_list.count(),
        "active_page": "potential",
    }
    return render(request, "stock/potential_page.html", context)


@login_required(login_url="/accounts/login/")
def short_term_page(request):
    """Trend page for display potential"""
    filter_params = {
        "is_day_fetched": True,
        "day_ema_200_1__lt": F("day_ema_20_1"),
        "day_ema_50_1__lt": F("day_ema_20_1"),
        "day_ha_open_1__lt": F("day_ha_close_1"),
        "day_ema_20_1__lt": F("day_ha_open_1"),
        "day_stoch_black_1__gt": 20,
        # "day_stoch_black_1__lt": 80,
    }
    total_stock = StockData.objects.all().count()
    annotate_params = {
        "day_stoch_cross_1": Case(
            When(
                Q(day_stoch_black_1__gt=F("day_stoch_red_1")) & Q(day_stoch_black_2__lt=F("day_stoch_red_2")),
                then=Value(True),
            ),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "rsi_cross_1": Case(
            When(Q(day_rsi_1__gt=60) & Q(day_rsi_2__lt=60), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    }
    day_stoch_list = (
        StockData.objects.annotate(**annotate_params).filter(**filter_params).order_by("day_stoch_black_1")
    )
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    context = {
        "title": "Day Stochastics",
        "stocks": day_stoch_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "short_term_count": day_stoch_list.count(),
        "active_page": "short_term",
    }
    return render(request, "stock/short_term_page.html", context)


@login_required(login_url="/accounts/login/")
def intraday_m15_positive_page(request):
    """Trend page for display potential"""
    total_stock = StockData.objects.filter(**potential_stock_filters).count()
    filter_params = {
        "is_m15_fetched": True,
        "m15_ha_close_1__gt": F("m15_ha_open_1"),
        "m15_ema_20_1__lt": F("m15_ha_close_1"),
        "m15_valid": True,
    }
    annotate_params = {
        "m15_ha_cross_1": Case(
            When(Q(m15_ema_20_1__lt=F("m15_ha_close_1")) & Q(m15_ema_20_1__gt=F("m15_ha_open_1")), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m15_ha_cross_2": Case(
            When(
                Q(m15_ema_20_1__lt=F("m15_ha_close_1"))
                & Q(m15_ema_20_1__lt=F("m15_ha_open_1"))
                & Q(m15_ema_20_2__gt=F("m15_ha_open_2")),
                then=Value(True),
            ),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m15_ema_cross_1": Case(
            When(m15_ema_50_1__lt=F("m15_ema_20_1"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m15_valid": Case(
            When(Q(m15_ema_20_1__lt=F("m15_ha_close_1")) & Q(m15_ema_20_1__gt=F("m15_ha_open_1")), then=Value(True)),
            When(
                Q(m15_ema_20_1__lt=F("m15_ha_close_1"))
                & Q(m15_ema_20_1__lt=F("m15_ha_open_1"))
                & Q(m15_ema_20_2__gt=F("m15_ha_open_2")),
                then=Value(True),
            ),
            default=Value(False),
            output_field=BooleanField(),
        ),
    }
    m15_positive_list = (
        StockData.objects.annotate(**annotate_params).filter(**potential_stock_filters).filter(**filter_params)
    )
    to_calculate = StockData.objects.filter(**potential_stock_filters).filter(is_m15_fetched=False).count()
    context = {
        "title": "15 Min Positive",
        "stocks": m15_positive_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "potential_count": m15_positive_list.count(),
        "active_page": "intraday",
    }
    return render(request, "stock/intraday_m15_positive_page.html", context)


@login_required(login_url="/accounts/login/")
def intraday_m15_negative_page(request):
    """Trend page for display potential"""
    total_stock = StockData.objects.all().count()
    filter_params = {
        "is_m15_fetched": True,
        "m15_ha_close_1__lt": F("m15_ha_open_1"),
        "m15_ema_20_1__gt": F("m15_ha_close_1"),
        "m15_valid": True,
    }
    annotate_params = {
        "m15_ha_cross_1": Case(
            When(Q(m15_ema_20_1__gt=F("m15_ha_close_1")) & Q(m15_ema_20_1__lt=F("m15_ha_open_1")), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m15_ha_cross_2": Case(
            When(
                Q(m15_ema_20_1__gt=F("m15_ha_close_1"))
                & Q(m15_ema_20_1__gt=F("m15_ha_open_1"))
                & Q(m15_ema_20_2__lt=F("m15_ha_open_2")),
                then=Value(True),
            ),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m15_ema_cross_1": Case(
            When(m15_ema_50_1__gt=F("m15_ema_20_1"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m15_valid": Case(
            When(Q(m15_ema_20_1__gt=F("m15_ha_close_1")) & Q(m15_ema_20_1__lt=F("m15_ha_open_1")), then=Value(True)),
            When(
                Q(m15_ema_20_1__gt=F("m15_ha_close_1"))
                & Q(m15_ema_20_1__gt=F("m15_ha_open_1"))
                & Q(m15_ema_20_2__lt=F("m15_ha_open_2")),
                then=Value(True),
            ),
            default=Value(False),
            output_field=BooleanField(),
        ),
    }
    m15_rsi_list = (
        StockData.objects.annotate(**annotate_params)
        .filter(**potential_negative_stock_filters)
        .filter(**filter_params)
    )
    to_calculate = StockData.objects.filter(is_m15_fetched=False).count()
    context = {
        "title": "15 Min Negative",
        "stocks": m15_rsi_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "potential_count": m15_rsi_list.count(),
        "active_page": "intraday",
    }
    return render(request, "stock/intraday_m15_negative_page.html", context)


@login_required(login_url="/accounts/login/")
def intraday_hourly_rsi_page(request):
    """Trend page for display potential"""
    total_stock = StockData.objects.filter(**potential_stock_filters).count()
    filter_params = {
        "is_day_fetched": True,
        "day_ha_open_1__lt": F("day_ha_close_1"),
        "is_hr_fetched": True,
        "hr_rsi_cross_1": True,
    }
    annotate_params = {
        "hr_rsi_cross_1": Case(
            When(Q(hr_rsi_1__gt=60) & Q(hr_rsi_2__lt=60), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    }
    hr_rsi_list = (
        StockData.objects.annotate(**annotate_params).filter(**potential_stock_filters).filter(**filter_params)
    )
    to_calculate = StockData.objects.filter(**potential_stock_filters).filter(is_hr_fetched=False).count()
    context = {
        "title": "Hourly RSI",
        "stocks": hr_rsi_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "potential_count": hr_rsi_list.count(),
        "active_page": "intraday",
    }
    return render(request, "stock/intraday_hr_rsi_page.html", context)


@login_required(login_url="/accounts/login/")
def intraday_daily_rsi_page(request):
    """Trend page for display potential"""
    total_stock = StockData.objects.filter(**potential_stock_filters).count()
    filter_params = {
        "is_day_fetched": True,
        "day_ha_open_1__lt": F("day_ha_close_1"),
        "day_rsi_1__gt": 60,
    }
    annotate_params = {
        "day_rsi_cross_1": Case(
            When(Q(day_rsi_1__gt=60) & Q(day_rsi_2__lt=60), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    }
    day_rsi_list = (
        StockData.objects.annotate(**annotate_params).filter(**potential_stock_filters).filter(**filter_params)
    )
    to_calculate = StockData.objects.filter(**potential_stock_filters).filter(is_day_fetched=False).count()
    context = {
        "title": "Daily RSI",
        "stocks": day_rsi_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "potential_count": day_rsi_list.count(),
        "active_page": "intraday",
    }
    return render(request, "stock/intraday_day_rsi_page.html", context)


@login_required(login_url="/accounts/login/")
def intraday_daily_stoch_page(request):
    """Trend page for display potential"""
    total_stock = StockData.objects.filter(**potential_stock_filters).count()
    filter_params = {
        "is_day_fetched": True,
        "day_ha_open_1__lt": F("day_ha_close_1"),
        "day_stoch_black_1__gt": 20,
        "day_stoch_black_1__lt": 80,
    }
    annotate_params = {
        "day_stoch_cross_1": Case(
            When(
                Q(day_stoch_black_1__gt=F("day_stoch_red_1")) & Q(day_stoch_black_2__lt=F("day_stoch_red_2")),
                then=Value(True),
            ),
            default=Value(False),
            output_field=BooleanField(),
        ),
    }
    day_stoch_list = (
        StockData.objects.annotate(**annotate_params).filter(**potential_stock_filters).filter(**filter_params)
    )
    to_calculate = StockData.objects.filter(**potential_stock_filters).filter(is_day_fetched=False).count()
    context = {
        "title": "Stochastics RSI",
        "stocks": day_stoch_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "potential_count": day_stoch_list.count(),
        "active_page": "intraday",
    }
    return render(request, "stock/intraday_day_stoch_page.html", context)


@login_required(login_url="/accounts/login/")
def trading_negative_page(request):
    """Trend page for display potential"""
    annotate_params = {
        "m5_1": Case(
            When(m5_ha_open_1__lt=F("m5_ha_close_1"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m5_2": Case(
            When(m5_ha_open_2__lt=F("m5_ha_close_2"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m5_3": Case(
            When(m5_ha_open_3__lt=F("m5_ha_close_3"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m5_ha_cross_1": Case(
            When(m5_ema_20_1__lt=F("m5_ha_close_1"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    }
    stock_list = StockData.objects.filter(is_trading=True).annotate(**annotate_params)
    latest_record = StockData.objects.latest("trading_updated_at")
    if request.method == "POST":
        form = TradingForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data["symbol"]
            stock_data = StockData.objects.get(symbol=symbol)
            if "_add" in request.POST:
                stock_data.is_trading = True
            elif "_remove" in request.POST:
                stock_data.is_trading = False
            stock_data.save()
            return redirect("trading")
    else:
        form = TradingForm()
    context = {
        "title": "Trading Negative",
        "form": form,
        "stocks": stock_list,
        "trading_updated_at": latest_record.trading_updated_at if latest_record else "",
    }
    return render(request, "stock/trading_negative_page.html", context)


def trend_page_load_live(request):
    """
    Load live stocks
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_live_stocks()
    trend_obj.create_trend()
    return redirect("configuration")


def trend_page_load_bhav(request):
    """
    Load bhav copy stocks
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_bhav_copy()
    trend_obj.create_trend()
    return redirect("configuration")


def trend_page_upload(request):
    pass


def trend_page_load_futures(request):
    """
    Load futures stocks
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    # trend_obj.fetch_futures_stocks()
    trend_obj.fetch_futures_stocks_smart()
    trend_obj.create_trend()
    return redirect("configuration")


def trend_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_trend_value(name)
    return redirect("configuration")


def potential_trend_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_potential_trend_value(name)
    return redirect("configuration")


def trading_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trading_m5_fetch(name)
    return redirect("configuration")


def trend_page_reset_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.trend_reset(name)
    return redirect("configuration")


def schedule_trading_start(request):
    schedule("mysuru.task.trading_m5_fetch", "m5", schedule_type=Schedule.MINUTES, minutes=5)
    return redirect("configuration")
