from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jrose.stock_data_fetch import (
    all_week_data_queryset,
    week_above_50_wma_queryset,
    week_above_50_wma_stoch_positive_queryset,
    all_day_data_queryset,
    week_above_50_wma_stoch_cross_queryset,
    week_above_50_wma_day_stoch_cross_queryset,
    week_above_50_wma_day_stoch_positive_queryset, day_above_50_wma_queryset,
)
from mysuru.models import StockData


@login_required(login_url="/accounts/login/")
def week_page(request):
    """Stocks Week View"""

    all_week_data = all_week_data_queryset()
    week_above_50_wma_data = week_above_50_wma_queryset()
    week_above_50_wma_stoch_cross_data = week_above_50_wma_stoch_cross_queryset()
    week_above_50_wma_stoch_positive_data = week_above_50_wma_stoch_positive_queryset()
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "week_page",
        # All Week data
        "all_week_data_list": all_week_data,
        "all_week_data_count": all_week_data.count(),
        # Week above 50 WMA
        "week_above_50_wma_data_list": week_above_50_wma_data,
        "week_above_50_wma_data_count": week_above_50_wma_data.count(),
        # Week above 50 WMA stochastic cross
        "week_above_50_wma_stoch_cross_data_list": week_above_50_wma_stoch_cross_data,
        "week_above_50_wma_stoch_cross_data_count": week_above_50_wma_stoch_cross_data.count(),
        # Week above 50 WMA stochastic positive
        "week_above_50_wma_stoch_positive_data_list": week_above_50_wma_stoch_positive_data,
        "week_above_50_wma_stoch_positive_data_count": week_above_50_wma_stoch_positive_data.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/week_page.html", context)


@login_required(login_url="/accounts/login/")
def day_page(request):
    """Stocks Day View"""

    all_day_data = all_day_data_queryset()
    week_above_50_wma_day_stoch_cross_data = week_above_50_wma_day_stoch_cross_queryset()
    week_above_50_wma_day_stoch_positive_data = week_above_50_wma_day_stoch_positive_queryset()
    day_above_50_wma_data = day_above_50_wma_queryset()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "day_page",
        # All Day data
        "all_day_data_list": all_day_data,
        "all_day_data_count": all_day_data.count(),
        # Week above 50 WMA Day stochastic cross
        "week_above_50_wma_day_stoch_cross_data_list": week_above_50_wma_day_stoch_cross_data,
        "week_above_50_wma_day_stoch_cross_data_count": week_above_50_wma_day_stoch_cross_data.count(),
        # Week above 50 WMA Day stochastic positive
        "week_above_50_wma_day_stoch_positive_data_list": week_above_50_wma_day_stoch_positive_data,
        "week_above_50_wma_day_stoch_positive_data_count": week_above_50_wma_day_stoch_positive_data.count(),
        # Day above 50 WMA
        "day_above_50_wma_data_list": day_above_50_wma_data,
        "day_above_50_wma_data_count": day_above_50_wma_data.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/day_page.html", context)


@login_required(login_url="/accounts/login/")
def smart_buy_page(request):
    """Stocks Smart View"""

    week_above_50_wma_stoch_cross_data = week_above_50_wma_stoch_cross_queryset()
    week_above_50_wma_day_stoch_cross_data = week_above_50_wma_day_stoch_cross_queryset()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "smart_buy_page",
        # Week above 50 WMA stochastic cross
        "week_above_50_wma_stoch_cross_data_list": week_above_50_wma_stoch_cross_data,
        "week_above_50_wma_stoch_cross_data_count": week_above_50_wma_stoch_cross_data.count(),
        # Week above 50 WMA Day stochastic cross
        "week_above_50_wma_day_stoch_cross_data_list": week_above_50_wma_day_stoch_cross_data,
        "week_above_50_wma_day_stoch_cross_data_count": week_above_50_wma_day_stoch_cross_data.count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/smart_buy_page.html", context)
