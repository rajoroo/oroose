from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jrose.stock_data_fetch import week_queryset
from mysuru.models import StockData


@login_required(login_url="/accounts/login/")
def week_page(request):
    """Stocks Day View"""

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


