from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from mysuru.models import StochDailyTrend, StochWeeklyTrend
from mysuru import polling_daily_stoch, polling_weekly_stoch


# ======================================Stoch Daily Page=======================================
@login_required(login_url="/accounts/login/")
def stoch_daily_page(request):
    stoch_list = StochDailyTrend.objects.filter(trend_status=True, stoch_status=True).order_by("d_value")
    valid_list = StochDailyTrend.objects.filter(trend_status=False, stoch_status=True).order_by("d_value")
    crossed_list = StochDailyTrend.objects.filter(crossed=True).order_by("d_value")

    weekly_data = StochWeeklyTrend.objects.filter(stoch_positive_trend=True).values_list("symbol", flat=True)
    daily_data = StochDailyTrend.objects.filter(crossed=True).values_list("symbol", flat=True)
    match_data = list(set(weekly_data) & set(daily_data))
    match_list = StochDailyTrend.objects.filter(symbol__in=match_data).order_by("d_value")

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
        {
            "title": "Crossed",
            "stoch_value": list(crossed_list.values()),
            "stoch_count": crossed_list.count(),
        },
        {
            "title": "Matched",
            "stoch_value": list(match_list.values()),
            "stoch_count": match_list.count(),
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
    positive_list = StochWeeklyTrend.objects.filter(stoch_positive_trend=True).order_by("d_value")
    crossed_list = StochWeeklyTrend.objects.filter(crossed=True).order_by("d_value")
    tend_positive_1_list = StochWeeklyTrend.objects.filter(tend_to_positive=True, d_trend=True).order_by("d_value")
    tend_positive_2_list = StochWeeklyTrend.objects.filter(tend_to_positive=True, d_trend=False).order_by("d_value")
    negative_list = StochWeeklyTrend.objects.filter(stoch_positive_trend=False).order_by("d_value")
    to_calculate = StochWeeklyTrend.objects.filter(
        date=datetime.today(), ema_200__isnull=True, smart_token__isnull=False
    ).count()
    stoch_result = [
        {
            "title": "Positive",
            "reference": "positive_stoch",
            "icon": "fa fa-solid fa-plus",
            "stoch_value": list(positive_list.values()),
            "stoch_count": positive_list.count(),
        },
        {
            "title": "Crossed",
            "reference": "crossed_stoch",
            "icon": "fa fa-solid fa-times",
            "stoch_value": list(crossed_list.values()),
            "stoch_count": crossed_list.count(),
        },
        {
            "title": "Tend to positive (1)",
            "reference": "tend_to_positive_1_stoch",
            "icon": "fa fa-solid fa-line-chart",
            "stoch_value": list(tend_positive_1_list.values()),
            "stoch_count": tend_positive_1_list.count(),
        },
        {
            "title": "Tend to positive (2)",
            "reference": "tend_to_positive_2_stoch",
            "icon": "fa fa-solid fa-level-up",
            "stoch_value": list(tend_positive_2_list.values()),
            "stoch_count": tend_positive_2_list.count(),
        },
        {
            "title": "Negative",
            "reference": "negative_stoch",
            "icon": "fa fa-solid fa-minus",
            "stoch_value": list(negative_list.values()),
            "stoch_count": negative_list.count(),
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
