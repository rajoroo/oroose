from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jrose.stock_data_fetch import (
    all_week_data_queryset,
    all_day_data_queryset,
    all_hr_data_queryset, daily_potential_queryset,
)
from mysuru.models import StockData


@login_required(login_url="/accounts/login/")
def week_page(request):
    """Stocks Week View"""

    all_week_data = all_week_data_queryset()
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "week_page",
        # All Week data
        "all_week_data_list": all_week_data,
        "all_week_data_count": all_week_data.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/week_page.html", context)


@login_required(login_url="/accounts/login/")
def day_page(request):
    """Stocks Day View"""

    all_day_data = all_day_data_queryset()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "day_page",
        # All Day data
        "all_day_data_list": all_day_data,
        "all_day_data_count": all_day_data.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/day_page.html", context)


@login_required(login_url="/accounts/login/")
def hr_page(request):
    """Stocks Hour View"""

    all_hr_data = all_hr_data_queryset()
    to_calculate = StockData.objects.filter(is_hr_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "day_page",
        # All Hour data
        "all_hr_data_list": all_hr_data,
        "all_hr_data_count": all_hr_data.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/hr_page.html", context)


@login_required(login_url="/accounts/login/")
def potential_page(request):
    """Day stochastic and Heikin ashi crossover"""
    stoch_data_list = daily_potential_queryset().filter(stoch_cross=True)
    ha_data_list = daily_potential_queryset().filter(ha_cross=True)
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "potential_page",
        # Stochastic data
        "stoch_data_list": stoch_data_list,
        "stoch_data_count": stoch_data_list.count(),
        # Heikinashi data
        "ha_data_list": ha_data_list,
        "ha_data_count": ha_data_list.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/potential_page.html", context)


@login_required(login_url="/accounts/login/")
def stoch_page(request):
    """Day stochastic crossover"""
    stoch_cross_list = daily_potential_queryset().filter(stoch_cross=True)
    stoch_positive_list = daily_potential_queryset().filter(stoch_postive=True)
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "stoch_page",
        # Stochastic cross
        "stoch_cross_list": stoch_cross_list,
        "stoch_cross_list_count": stoch_cross_list.count(),
        # Stochastic positive
        "stoch_positive_list": stoch_positive_list,
        "stoch_positive_list_count": stoch_positive_list.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/stoch_page.html", context)


@login_required(login_url="/accounts/login/")
def rsi_page(request):
    """RSI Page"""
    rsi_list = StockData.objects.filter(is_day_fetched=True, day_rsi_0__gt=50).order_by("day_rsi_0")
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "rsi_page",
        # RSI
        "rsi_list": rsi_list,
        "rsi_count": rsi_list.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,

    }
    return render(request, "stock/rsi_page.html", context)


