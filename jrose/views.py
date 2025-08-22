from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jrose.stock_data_fetch import (
    all_week_data_queryset,
    all_day_data_queryset,
    wk_ha_0_cross,
    wk_ha_1_cross,
    wk_close_below_ha_0_green_open,
    wk_close_below_ha_0_red_open,
    wk_close_above_ha_0_red_open,
    wk_ha_0_green,
    wk_ha_0_red,
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
def potential_page(request):
    """Day stochastic and Heikin ashi crossover"""

    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "potential_page",
        # Week Heikin Ashi 0 Cross
        "wk_ha_0_cross_list": wk_ha_0_cross(),
        "wk_ha_0_cross_count": wk_ha_0_cross().count(),
        # Week Heikin Ashi 1 Cross
        "wk_ha_1_cross_list": wk_ha_1_cross(),
        "wk_ha_1_cross_count": wk_ha_1_cross().count(),
        # Week Close Below Heikin Ashi 0 Green Open
        "wk_close_below_ha_0_green_open_list": wk_close_below_ha_0_green_open(),
        "wk_close_below_ha_0_green_open_count": wk_close_below_ha_0_green_open().count(),
        # Week Close Below Heikin Ashi 0 Red Open
        "wk_close_below_ha_0_red_open_list": wk_close_below_ha_0_red_open(),
        "wk_close_below_ha_0_red_open_count": wk_close_below_ha_0_red_open().count(),
        # Week Close Above Heikin Ashi 0 Red Open
        "wk_close_above_ha_0_red_open_list": wk_close_above_ha_0_red_open(),
        "wk_close_above_ha_0_red_open_count": wk_close_above_ha_0_red_open().count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/potential_page.html", context)


@login_required(login_url="/accounts/login/")
def heikinashi_page(request):
    """Day stochastic and Heikin ashi crossover"""

    to_calculate = StockData.objects.filter(is_wk_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "heikinashi_page",
        # Heikin Ashi 0 Green
        "wk_ha_0_green_list": wk_ha_0_green(),
        "wk_ha_0_green_count": wk_ha_0_green().count(),
        # Heikin Ashi O Red
        "wk_ha_0_red_list": wk_ha_0_red(),
        "wk_ha_0_red_count": wk_ha_0_red().count(),
        # Total Count
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/heikinashi_page.html", context)
