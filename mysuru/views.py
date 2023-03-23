from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from mysuru.models import TopTen, TrendStatus, MacdTrend
from mysuru.polling_top_ten import polling_top_ten_stocks, trigger_calculate_top_ten


# Uptrend
@login_required(login_url="/accounts/login/")
def mysuru_page(request):
    top_10 = TopTen.objects.filter(is_valid=True)
    to_calculate = TopTen.objects.filter(date=datetime.today(), ema_200__isnull=True).count()
    context = {
        "active_page": "mysuru",
        "top_10": list(top_10.values()),
        "to_calculate": to_calculate,
    }
    return render(request, "mysuru/base_page.html", context)


def mysuru_load_top_ten(request):
    polling_top_ten_stocks()
    return HttpResponse(status=200)


def mysuru_calculate_top_ten(request):
    trigger_calculate_top_ten()
    return HttpResponse(status=200)


# Uptrend
@login_required(login_url="/accounts/login/")
def macd_page(request):
    macd_list = MacdTrend.objects.filter(trend_status=TrendStatus.YES)
    to_calculate = MacdTrend.objects.filter(date=datetime.today(), ema_200__isnull=True).count()
    context = {
        "active_page": "macd",
        "macds": list(macd_list.values()),
        "macd_count": macd_list.count(),
        "to_calculate": to_calculate,
    }
    return render(request, "macd/base_page.html", context)


def load_macd_page(request):
    polling_top_ten_stocks()
    return HttpResponse(status=200)


def calculate_macd_page(request):
    trigger_calculate_top_ten()
    return HttpResponse(status=200)
