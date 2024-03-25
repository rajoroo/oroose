from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import F

from mysuru.fetch_trend import get_model_object, FetchTrend
from mysuru.models import HourlyTrend, WeeklyTrend


# =========================================Trend==========================================
@login_required(login_url="/accounts/login/")
def trend_page(request, name):
    """Trend page for display Hourly/ Daily/ Weekly"""
    model_obj = get_model_object(name)
    total_stock = model_obj.objects.all().count()
    all_stock_list = model_obj.objects.all()
    to_calculate = model_obj.objects.filter(is_fetched=False).count()
    ha_cross_ma_20 = model_obj.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open__lt=F("ha_close"),
        ema_20__lt=F("ha_close"),
    )
    items = [
        {
            "title": "All Stocks",
            "stocks": all_stock_list,
            "count": all_stock_list.count(),
        },
        {
            "title": "20 Moving average crossed",
            "description": """Helsinki-asli cross the 20 moving average""",
            "stocks": ha_cross_ma_20,
            "count": ha_cross_ma_20.count(),
        },
    ]
    context = {
        "page_title": name.upper(),
        "active_page": "trend_page",
        "active_path": name,
        "items": items,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "trend/base_page.html", context)


def trend_page_load_live(request, name):
    """
    Load live stocks
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.fetch_live_stocks()
    trend_obj.create_trend()
    return redirect("trend_page", name=name)


def trend_page_load_bhav(request, name):
    """
    Load bhav copy stocks
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.fetch_bhav_copy()
    trend_obj.create_trend()
    return redirect("trend_page", name=name)


def trend_page_upload(request, name):
    pass


def trend_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.fetch_trend_value()
    return redirect("trend_page", name=name)


def trend_page_reset(request, name):
    """
    Reset trend model to fetch form the API
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.reset_fetched()
    return redirect("trend_page", name=name)


def potential_page(request):
    total_stock = WeeklyTrend.objects.all().count()
    to_calculate = WeeklyTrend.objects.filter(is_fetched=False).count()
    potential_stocks = WeeklyTrend.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open__lt=F("ha_close"),
        stoch_black__gt=F("stoch_red"),
        stoch_black__gte=20,
        stoch_black__lte=80,
    )
    items = [
        {
            "title": "Stocks",
            "stocks": potential_stocks,
            "count": potential_stocks.count(),
        },
    ]
    context = {
        "page_title": "POTENTIAL",
        "active_page": "potential_page",
        "active_path": None,
        "items": items,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "trend/base_page.html", context)


def short_term_page(request):
    total_stock = HourlyTrend.objects.all().count()
    to_calculate = HourlyTrend.objects.filter(is_fetched=False).count()
    potential_stocks = HourlyTrend.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open__lt=F("ha_close"),
        ema_20__lt=F("ha_close"),
    )
    items = [
        {
            "title": "Stocks",
            "stocks": potential_stocks,
            "count": potential_stocks.count(),
        },
    ]
    context = {
        "page_title": "SHORT TERM",
        "active_page": "short_term_page",
        "active_path": None,
        "items": items,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "trend/base_page.html", context)
