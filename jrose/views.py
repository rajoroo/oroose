from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jrose.stock_data_fetch import week_queryset, day_queryset, smart_buy_week_queryset, smart_buy_day_queryset, \
    smart_buy_potential_queryset
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

    stock_week_qs = smart_buy_week_queryset()
    stock_day_qs = smart_buy_day_queryset()
    stock_potential_qs = smart_buy_potential_queryset()
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "smart_buy_page",
        "stock_week_list": stock_week_qs,
        "stock_week_count": stock_week_qs.count(),
        "stock_day_list": stock_day_qs,
        "stock_day_count": stock_day_qs.count(),
        "stock_potential_list": stock_potential_qs,
        "stock_potential_count": stock_potential_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/smart_buy_page.html", context)

