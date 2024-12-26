from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jrose.stock_data_fetch import (
    week_queryset,
    day_queryset,
    smart_buy_week_stoch_cross_queryset,
    smart_buy_day_stoch_cross_queryset,
    smart_buy_day_wma_cross_queryset,
    smart_buy_day_above_wma_queryset, week_above_wma_queryset,
)
from mysuru.models import StockData
from django.db.models import F


@login_required(login_url="/accounts/login/")
def week_page(request):
    """Stocks Week View"""

    stock_qs = week_queryset()
    stoch_positive_qs = week_queryset().filter(wk_stoch_black_0__gt=F("wk_stoch_red_0")).order_by("wk_stoch_black_0")
    stoch_wk_above_wma_qs = week_above_wma_queryset()
    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "week_page",
        "stock_list": stock_qs,
        "stock_count": stock_qs.count(),
        "stoch_positive_list": stoch_positive_qs,
        "stoch_positive_count": stoch_positive_qs.count(),
        "stoch_wk_above_wma_list": stoch_wk_above_wma_qs,
        "stoch_wk_above_wma_count": stoch_wk_above_wma_qs.count(),
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
    stoch_day_stoch_cross_qs = smart_buy_day_stoch_cross_queryset()
    stoch_day_wma_cross_qs = smart_buy_day_wma_cross_queryset()
    stoch_day_above_wma_qs = smart_buy_day_above_wma_queryset()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "smart_buy_page",
        # Week Cross
        "stock_week_stoch_cross_list": stock_week_stoch_cross_qs,
        "stock_week_stoch_cross_count": stock_week_stoch_cross_qs.count(),
        # Day Cross
        "stock_day_stoch_cross_list": stoch_day_stoch_cross_qs,
        "stock_day_stoch_cross_count": stoch_day_stoch_cross_qs.count(),
        # Day Cross WMA 20
        "stock_day_wma_cross_list": stoch_day_wma_cross_qs,
        "stock_day_wma_cross_count": stoch_day_wma_cross_qs.count(),
        # Day above WMA 20
        "stock_day_above_wmq_list": stoch_day_above_wma_qs,
        "stock_day_above_wma_count": stoch_day_above_wma_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/smart_buy_page.html", context)
