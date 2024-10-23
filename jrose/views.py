from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mysuru.models import StockData
from jrose.stock_data_fetch import smart_buy_queryset, hour_queryset


@login_required(login_url="/accounts/login/")
def day_page(request):
    """Stocks Day View"""

    stock_qs = smart_buy_queryset().order_by("day_stoch_black_0")
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
def hour_page(request):
    """Stocks Hour View"""

    stock_qs = hour_queryset()
    to_calculate = StockData.objects.filter(is_hr_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "hr_page",
        "stock_list": stock_qs,
        "stock_count": stock_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/hr_page.html", context)


@login_required(login_url="/accounts/login/")
def smart_buy_view(request):
    """Smart Buy Stocks"""

    rsi_cross_qs = smart_buy_queryset().filter(day_rsi_cross=True)
    ha_cross_qs = smart_buy_queryset().filter(day_ha_cross=True)
    stoch_cross_qs = smart_buy_queryset().filter(day_stoch_cross=True).order_by("day_stoch_black_0")
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "smart_buy",
        "rsi_cross_list": rsi_cross_qs,
        "rsi_cross_count": rsi_cross_qs.count(),
        "ha_cross_list": ha_cross_qs,
        "ha_cross_count": ha_cross_qs.count(),
        "stoch_cross_list": stoch_cross_qs,
        "stoch_cross_count": stoch_cross_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/smart_buy_page.html", context)
