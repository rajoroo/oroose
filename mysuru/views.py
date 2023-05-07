from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from mysuru.models import MacdTrend
from mysuru.polling_macd import polling_macd_stocks, trigger_calculate_macd


@login_required(login_url="/accounts/login/")
def macd_page(request):
    day_1_list = MacdTrend.objects.filter(trend_status=True, day_1_status=True)
    day_2_list = MacdTrend.objects.filter(trend_status=True, day_1_status=False, day_2_status=True)
    valid_list = MacdTrend.objects.filter(
        Q(day_1_status=True, trend_status=False) | Q(day_2_status=True, trend_status=False)
    ).order_by("ema_200_percentage")
    to_calculate = MacdTrend.objects.filter(
        date=datetime.today(), ema_200__isnull=True, smart_token__isnull=False
    ).count()
    macd_result = [
        {
            "title": "Day 1",
            "macd_value": list(day_1_list.values()),
            "macd_count": day_1_list.count(),
        },
        {
            "title": "Day 2",
            "macd_value": list(day_2_list.values()),
            "macd_count": day_2_list.count(),
        },
        {
            "title": "Valid",
            "macd_value": list(valid_list.values()),
            "macd_count": valid_list.count(),
        },
    ]
    context = {
        "active_page": "macd",
        "macd_result": macd_result,
        "to_calculate": to_calculate,
    }
    return render(request, "macd/base_page.html", context)


def load_macd_page(request):
    polling_macd_stocks()
    return redirect("macd")


def calculate_macd_page(request):
    trigger_calculate_macd()

    return JsonResponse({"status": "success", "message": "Successfully Calculated"})
