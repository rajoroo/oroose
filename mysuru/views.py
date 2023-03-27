from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mysuru.models import TopTen, TrendStatus, MacdTrend
from mysuru.polling_top_ten import polling_top_ten_stocks, trigger_calculate_top_ten
from mysuru.polling_macd import polling_macd_stocks, trigger_calculate_macd
from django.http import JsonResponse


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

    return JsonResponse({
        "status": "success",
        "message": "Successfully loaded the content"
    })


def mysuru_calculate_top_ten(request):
    trigger_calculate_top_ten()

    return JsonResponse({
        "status": "success",
        "message": "Successfully Calculated"
    })


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
    polling_macd_stocks()

    return JsonResponse({
        "status": "success",
        "message": "Successfully loaded the content"
    })


def calculate_macd_page(request):
    trigger_calculate_macd()

    return JsonResponse({
        "status": "success",
        "message": "Successfully Calculated"
    })
