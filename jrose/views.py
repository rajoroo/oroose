from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from mysuru.models import StockData
from jrose.stock_data_fetch import m15_positive_queryset, m15_negative_queryset, daily_potential_queryset


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
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()
    stock_list = [
        {
            "title": "Daily Potential",
            "stocks": stocks,
            "stock_count": stocks.count(),
            "help": "Daily Potential stocks"
        },
    ]
    context = {
        "active_page": "daily_potential",
        "stock_list": stock_list,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/daily_potential.html", context)
