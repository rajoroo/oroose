from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mysuru.models import StockData
from jrose.stock_data_fetch import smart_buy_queryset


@login_required(login_url="/accounts/login/")
def smart_buy_view(request):
    """Smart Buy Stocks"""

    rsi_cross_qs = smart_buy_queryset().filter(day_rsi_cross=True)
    ha_cross_qs = smart_buy_queryset().filter(day_ha_cross=True)
    day_rsi_above_60_qs = smart_buy_queryset().filter(wk_rsi_0__gt=60)
    m15_positive_qs = smart_buy_queryset().filter(wk_rsi_0__gt=60, m15_positive=True)
    to_calculate = StockData.objects.filter(is_day_fetched=False).count()
    total_stock = StockData.objects.filter().all().count()

    context = {
        "active_page": "smart_buy",
        "rsi_cross_list": rsi_cross_qs,
        "rsi_cross_count": rsi_cross_qs.count(),
        "ha_cross_list": ha_cross_qs,
        "ha_cross_count": ha_cross_qs.count(),
        "day_rsi_above_60_list": day_rsi_above_60_qs,
        "day_rsi_above_60_count": day_rsi_above_60_qs.count(),
        "m15_positive_list": m15_positive_qs,
        "m15_positive_count": m15_positive_qs.count(),
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stock/smart_buy_page.html", context)
