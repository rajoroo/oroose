from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import F, Q, Case, When, Value, BooleanField

from mysuru.fetch_trend import FetchTrend
from mysuru.models import StockData
from datetime import datetime


# =========================================Fiters=========================================
potential_stock_filters = {
    "is_wk_fetched": True,
    "wk_ema_200_1__lt": F("wk_ema_20_1"),
    "wk_ema_50_1__lt": F("wk_ema_20_1"),
    "wk_ha_open_1__lt": F("wk_ha_close_1"),
    "wk_ema_20_1__lt": F("wk_ha_open_1"),
    "wk_rsi_1__gt": 60,
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
            "wk_rsi_0__gt": 60,
        }
        annotate_params = {
            "ha_cross_0": Case(
                When(Q(wk_ha_open_0__lt=F("wk_ha_close_0")) & Q(wk_ha_open_1__gt=F("wk_ha_close_1")), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            "rsi_cross_0": Case(
                When(Q(wk_rsi_0__gt=60) & Q(wk_rsi_1__lt=60), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
        }
    else:
        filter_params = {
            "is_wk_fetched": True,
            "wk_ema_200_1__lt": F("wk_ema_20_1"),
            "wk_ema_50_1__lt": F("wk_ema_20_1"),
            "wk_ha_open_1__lt": F("wk_ha_close_1"),
            "wk_ema_20_1__lt": F("wk_ha_open_1"),
            "wk_rsi_1__gt": 60,
        }
        annotate_params = {
            "ha_cross_1": Case(
                When(Q(wk_ha_open_1__lt=F("wk_ha_close_1")) & Q(wk_ha_open_2__gt=F("wk_ha_close_2")), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            "rsi_cross_1": Case(
                When(Q(wk_rsi_1__gt=60) & Q(wk_rsi_2__lt=60), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
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
def intraday_m15_rsi_page(request):
    """Trend page for display potential"""
    total_stock = StockData.objects.filter(**potential_stock_filters).count()
    filter_params = {
        "is_day_fetched": True,
        "day_ha_open_1__lt": F("day_ha_close_1"),
        "is_m15_fetched": True,
        "m15_rsi_cross_1": True,
    }
    annotate_params = {
        "m15_rsi_cross_1": Case(
            When(Q(m15_rsi_1__gt=60) & Q(m15_rsi_2__lt=60), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
    }
    m15_rsi_list = StockData.objects.annotate(**annotate_params).filter(**potential_stock_filters).filter(**filter_params)
    to_calculate = StockData.objects.filter(**potential_stock_filters).filter(is_m15_fetched=False).count()
    context = {
        "title": "15 Min RSI",
        "stocks": m15_rsi_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "potential_count": m15_rsi_list.count(),
        "active_page": "intraday",
    }
    return render(request, "stock/intraday_m15_rsi_page.html", context)


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
            output_field=BooleanField()
        ),
    }
    hr_rsi_list = StockData.objects.annotate(**annotate_params).filter(**potential_stock_filters).filter(**filter_params)
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
            output_field=BooleanField()
        ),
    }
    day_rsi_list = StockData.objects.annotate(**annotate_params).filter(**potential_stock_filters).filter(**filter_params)
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
            When(Q(day_stoch_black_1__gt=F("day_stoch_red_1")) & Q(day_stoch_black_2__lt=F("day_stoch_red_2")), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
    }
    day_stoch_list = StockData.objects.annotate(**annotate_params).filter(**potential_stock_filters).filter(**filter_params)
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
    trend_obj.fetch_futures_stocks()
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


def trend_page_reset_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.trend_reset(name)
    return redirect("configuration")
