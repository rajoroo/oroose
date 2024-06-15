from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import F

from mysuru.fetch_trend import FetchTrend
from mysuru.models import StockData
from datetime import datetime


# =========================================Trend==========================================
@login_required(login_url="/accounts/login/")
def stock_data_week_page(request):
    """Trend page for display Weekly"""
    total_stock = StockData.objects.all().count()
    all_stock_list = StockData.objects.all()
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    record_type = True if datetime.today().weekday() > 4 else False
    context = {
        "title": "Weekly",
        "stocks": all_stock_list,
        "record_type": record_type,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "active_page": "stock_data",
    }
    return render(request, "stock/weekly_page.html", context)


@login_required(login_url="/accounts/login/")
def stock_data_day_page(request):
    """Trend page for display Weekly"""
    total_stock = StockData.objects.all().count()
    all_stock_list = StockData.objects.all()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    record_type = True if datetime.today().weekday() > 4 else False
    context = {
        "title": "Daily",
        "stocks": all_stock_list,
        "record_type": record_type,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
        "active_page": "stock_data",
    }
    return render(request, "stock/day_page.html", context)


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
    else:
        filter_params = {
            "is_wk_fetched": True,
            "wk_ema_200_1__lt": F("wk_ema_20_1"),
            "wk_ema_50_1__lt": F("wk_ema_20_1"),
            "wk_ha_open_1__lt": F("wk_ha_close_1"),
            "wk_ema_20_1__lt": F("wk_ha_open_1"),
            "wk_rsi_1__gt": 60,
        }
    potential_stock_list = StockData.objects.filter(**filter_params)
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

