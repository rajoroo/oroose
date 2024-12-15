from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jrose.stock_data_fetch import (
    week_queryset,
    day_queryset,
    smart_buy_week_above_wma_queryset,
    smart_buy_week_stoch_cross_queryset,
    smart_buy_week_rsi_cross_queryset,
    smart_buy_week_wma_cross_queryset,
    smart_buy_day_stoch_cross_queryset
)
from mysuru.models import StockData


@login_required(login_url="/accounts/login/")
def week_page(request):
    """Stocks Week View"""

    stock_qs = week_queryset()
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "week_page",
        "stock_list": stock_qs,
        "stock_count": stock_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/week_page.html", context)


@login_required(login_url="/accounts/login/")
def day_page(request):
    """Stocks Day View"""

    stock_qs = day_queryset()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "day_page",
        "stock_list": stock_qs,
        "stock_count": stock_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/day_page.html", context)


@login_required(login_url="/accounts/login/")
def smart_buy_page(request):
    """Stocks Smart View"""

    stock_week_stoch_cross_qs = smart_buy_week_stoch_cross_queryset()
    stoch_week_rsi_cross_qs = smart_buy_week_rsi_cross_queryset()
    stoch_week_wma_cross_qs = smart_buy_week_wma_cross_queryset()
    stoch_week_above_wma_qs = smart_buy_week_above_wma_queryset()
    stoch_day_stoch_cross_qs = smart_buy_day_stoch_cross_queryset()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "smart_buy_page",
        # Week Cross
        "stock_week_stoch_cross_list": stock_week_stoch_cross_qs,
        "stock_week_stoch_cross_count": stock_week_stoch_cross_qs.count(),
        # Week RSI above 60
        "stock_week_rsi_cross_list": stoch_week_rsi_cross_qs,
        "stock_week_rsi_cross_count": stoch_week_rsi_cross_qs.count(),
        # Week Cross WMA 20
        "stock_week_wma_cross_list": stoch_week_wma_cross_qs,
        "stock_week_wma_cross_count": stoch_week_wma_cross_qs.count(),
        # Week above WMA 20
        "stock_week_above_wmq_list": stoch_week_above_wma_qs,
        "stock_week_above_wma_count": stoch_week_above_wma_qs.count(),
        # Day Cross
        "stock_day_stoch_cross_list": stoch_day_stoch_cross_qs,
        "stock_day_stoch_cross_count": stoch_day_stoch_cross_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/smart_buy_page.html", context)

