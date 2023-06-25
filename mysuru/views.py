from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from mysuru.models import MacdTrend, StochDailyTrend, StochWeeklyTrend
from mysuru import polling_macd, polling_daily_stoch, polling_weekly_stoch


# ======================================Stoch Daily Page=======================================
@login_required(login_url="/accounts/login/")
def stoch_daily_page(request):
    stoch_list = StochDailyTrend.objects.filter(trend_status=True, stoch_status=True)
    valid_list = StochDailyTrend.objects.filter(trend_status=False, stoch_status=True).order_by("ema_200_percentage")
    to_calculate = StochDailyTrend.objects.filter(
        date=datetime.today(), ema_200__isnull=True, smart_token__isnull=False
    ).count()
    stoch_result = [
        {
            "title": "Status",
            "stoch_value": list(stoch_list.values()),
            "stoch_count": stoch_list.count(),
        },
        {
            "title": "Valid",
            "stoch_value": list(valid_list.values()),
            "stoch_count": valid_list.count(),
        },
    ]
    context = {
        "active_page": "stoch_daily",
        "stoch_result": stoch_result,
        "to_calculate": to_calculate,
    }
    return render(request, "stoch_daily/base_page.html", context)


def load_stoch_daily_page(request):
    polling_daily_stoch.polling_stoch_stocks()
    return redirect("stoch_daily")


def calculate_stoch_daily_page(request):
    polling_daily_stoch.trigger_calculate_stoch()

    return JsonResponse({"status": "success", "message": "Successfully Calculated"})


# ======================================Stoch Weekly Page=======================================
@login_required(login_url="/accounts/login/")
def stoch_weekly_page(request):
    stoch_list = StochWeeklyTrend.objects.filter(trend_status=True, stoch_status=True)
    valid_list = StochWeeklyTrend.objects.filter(trend_status=False, stoch_status=True).order_by("ema_200_percentage")
    positive_list = StochWeeklyTrend.objects.filter(stoch_positive_trend=True).order_by("d_value")
    weekly_data = StochWeeklyTrend.objects.filter(stoch_positive_trend=True).values_list("symbol", flat=True)
    daily_data = StochDailyTrend.objects.filter(stoch_positive_trend=True).values_list("symbol", flat=True)
    match_data = list(set(weekly_data) & set(daily_data))
    match_list = StochDailyTrend.objects.filter(symbol__in=match_data).order_by("d_value")
    to_calculate = StochWeeklyTrend.objects.filter(
        date=datetime.today(), ema_200__isnull=True, smart_token__isnull=False
    ).count()
    stoch_result = [
        {
            "title": "Status",
            "stoch_value": list(stoch_list.values()),
            "stoch_count": stoch_list.count(),
        },
        {
            "title": "Valid",
            "stoch_value": list(valid_list.values()),
            "stoch_count": valid_list.count(),
        },
        {
            "title": "Positive",
            "stoch_value": list(positive_list.values()),
            "stoch_count": positive_list.count(),
        },
        {
            "title": "Match (Daily)",
            "stoch_value": list(match_list.values()),
            "stoch_count": match_list.count(),
        },
    ]
    context = {
        "active_page": "stoch_weekly",
        "stoch_result": stoch_result,
        "to_calculate": to_calculate,
    }
    return render(request, "stoch_weekly/base_page.html", context)


def load_stoch_weekly_page(request):
    polling_weekly_stoch.polling_stoch_stocks()
    return redirect("stoch_weekly")


def calculate_stoch_weekly_page(request):
    polling_weekly_stoch.trigger_calculate_stoch()

    return JsonResponse({"status": "success", "message": "Successfully Calculated"})


# ======================================Macd daily Page=======================================
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
    polling_macd.polling_macd_stocks()
    return redirect("macd")


def calculate_macd_page(request):
    polling_macd.trigger_calculate_macd()

    return JsonResponse({"status": "success", "message": "Successfully Calculated"})
