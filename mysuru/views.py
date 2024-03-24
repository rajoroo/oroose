from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.db.models import F

from mysuru.models import StochHourlyTrend, StochDailyTrend, StochWeeklyTrend
from mysuru import polling_hourly_stoch, polling_daily_stoch, polling_weekly_stoch, polling_futures
from django.views.decorators.csrf import csrf_exempt
from home.forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django_q.models import Schedule
from django_q.tasks import schedule


# ======================================Stoch Hourly Page=======================================
@login_required(login_url="/accounts/login/")
def stoch_hourly_page(request):
    all_stock_list = StochHourlyTrend.objects.all().order_by("d_value")
    ha_wma_cross_last_hour = StochHourlyTrend.objects.filter(ha_wma_cross_last_hour=True, ha_wma_top=True).order_by(
        "d_value"
    )
    total_stock = StochHourlyTrend.objects.all().count()
    to_calculate = StochHourlyTrend.objects.filter(
        date=datetime.today(), ema_200__isnull=True, smart_token__isnull=False
    ).count()
    stoch_result = [
        {
            "title": "All Stocks",
            "stoch_value": list(all_stock_list.values()),
            "stoch_count": all_stock_list.count(),
        },
        {
            "title": "HA WMA Cross Last Hour",
            "reference": "ha_top",
            "icon": "fa fa-solid fa-level-up",
            "stoch_value": list(ha_wma_cross_last_hour.values()),
            "stoch_count": ha_wma_cross_last_hour.count(),
        },
    ]
    context = {
        "active_page": "stoch_hourly",
        "stoch_result": stoch_result,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stoch_hourly/base_page.html", context)


def load_stoch_hourly_page(request):
    polling_hourly_stoch.polling_stoch_stocks()
    return redirect("stoch_hourly")


@csrf_exempt
def upload_hourly_stock_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            polling_hourly_stoch.handle_upload_stoch_stocks(request.FILES["file"])
            return HttpResponseRedirect(reverse("stoch_hourly"))
    else:
        form = UploadFileForm()
    rendered = render_to_string("stoch_hourly/file_upload.html", {"form": form, "title": "Upload Stocks"})
    response = HttpResponse(rendered)
    return response


def load_bhav_stoch_hourly_page(request):
    polling_hourly_stoch.polling_bhav_copy()
    return redirect("stoch_hourly")


def reset_calculate_stoch_hourly_page(request):
    StochHourlyTrend.objects.all().update(ema_200=None)
    return JsonResponse({"status": "success", "message": "Successfully Reset Calculated"})


def calculate_stoch_hourly_page(request):
    polling_hourly_stoch.trigger_calculate_stoch()

    return JsonResponse({"status": "success", "message": "Successfully Calculated"})


# ======================================Stoch Daily Page=======================================
@login_required(login_url="/accounts/login/")
def stoch_daily_page(request):
    all_stock_list = StochDailyTrend.objects.filter(stoch_positive_trend=True).order_by("d_value")
    ha_wma_cross_yesterday = StochDailyTrend.objects.filter(ha_wma_cross_yesterday=True, ha_wma_top=True).order_by(
        "d_value"
    )
    potential_stock = StochDailyTrend.objects.filter(
        stoch_positive_trend=True, ema_200_percentage__lt=0, d_value__range=[20, 80]
    ).order_by("d_value")
    total_stock = StochDailyTrend.objects.all().count()
    to_calculate = StochDailyTrend.objects.filter(
        date=datetime.today(), ema_200__isnull=True, smart_token__isnull=False
    ).count()
    stoch_result = [
        {
            "title": "All Stocks",
            "stoch_value": list(all_stock_list.values()),
            "stoch_count": all_stock_list.count(),
        },
        {
            "title": "HA WMA Cross Yesterday",
            "reference": "ha_top",
            "icon": "fa fa-solid fa-level-up",
            "stoch_value": list(ha_wma_cross_yesterday.values()),
            "stoch_count": ha_wma_cross_yesterday.count(),
        },
        {
            "title": "Potential Positive",
            "reference": "positive_stoch",
            "icon": "fa fa-solid fa-plus",
            "stoch_value": list(potential_stock.values()),
            "stoch_count": potential_stock.count(),
        },
    ]
    context = {
        "active_page": "stoch_daily",
        "stoch_result": stoch_result,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "stoch_daily/base_page.html", context)


def load_stoch_daily_page(request):
    polling_daily_stoch.polling_stoch_stocks()
    return redirect("stoch_daily")


@csrf_exempt
def upload_daily_stock_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            polling_daily_stoch.handle_upload_stoch_stocks(request.FILES["file"])
            return HttpResponseRedirect(reverse("stoch_daily"))
    else:
        form = UploadFileForm()
    rendered = render_to_string("stoch_daily/file_upload.html", {"form": form, "title": "Upload Stocks"})
    response = HttpResponse(rendered)
    return response


def load_bhav_stoch_daily_page(request):
    polling_daily_stoch.polling_bhav_copy()
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
    total_stock = StochWeeklyTrend.objects.all().count()
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
        "total_stock": total_stock,
    }
    return render(request, "stoch_weekly/base_page.html", context)


def load_stoch_weekly_page(request):
    print("i call -----")
    polling_weekly_stoch.polling_stoch_stocks()
    return redirect("stoch_weekly")


@csrf_exempt
def upload_weekly_stock_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            polling_weekly_stoch.handle_upload_stoch_stocks(request.FILES["file"])
            return HttpResponseRedirect(reverse("stoch_weekly"))
    else:
        form = UploadFileForm()
    rendered = render_to_string("stoch_weekly/file_upload.html", {"form": form, "title": "Upload Stocks"})
    response = HttpResponse(rendered)
    return response


def load_bhav_stoch_weekly_page(request):
    polling_weekly_stoch.polling_bhav_copy()
    return redirect("stoch_weekly")


def load_futures_stoch_weekly_page(request):
    polling_futures.polling_futures_stocks()
    return redirect("stoch_weekly")


def load_eligible_futures_stoch_weekly_page(request):
    recs = StochWeeklyTrend.objects.filter(ema_50__gt=F("ema_200"))
    StochHourlyTrend.objects.all().delete()
    for rec in recs:
        tt = StochHourlyTrend.objects.create(
            date=datetime.today(),
            symbol=rec.symbol,
            identifier=rec.identifier,
            isin=rec.isin,
            company_name=rec.company_name,
            # ema_200=rec.ema_200,
            # updated_date=datetime.today(),
        )
        tt.get_smart_token()
    return redirect("stoch_weekly")


def load_schedule_futures_stoch_weekly_page(request):
    Schedule.objects.all().delete()
    schedule(
        func="mysuru.views.run_schedule_futures", schedule_type=Schedule.CRON, cron="20 9,10,11,12,13,14,15 * * 1-5"
    )
    return redirect("stoch_weekly")


def run_schedule_futures():
    print("=====scheduler start=====")
    polling_daily_stoch.trigger_calculate_stoch()
    print("=====scheduler stop=====")
    return True


def calculate_stoch_weekly_page(request):
    polling_weekly_stoch.trigger_calculate_stoch()

    return JsonResponse({"status": "success", "message": "Successfully Calculated"})


# ============================= Potential stocks page ==============================
@login_required(login_url="/accounts/login/")
def potential_stock_page(request):
    positive_list = StochWeeklyTrend.objects.filter(
        stoch_positive_trend=True, ema_200_percentage__lt=0, d_value__range=[20, 80]
    ).order_by("d_value")
    to_calculate = StochWeeklyTrend.objects.filter(
        date=datetime.today(), ema_200__isnull=True, smart_token__isnull=False
    ).count()
    stoch_result = [
        {
            "title": "Potential Positive",
            "reference": "positive_stoch",
            "icon": "fa fa-solid fa-plus",
            "stoch_value": list(positive_list.values()),
            "stoch_count": positive_list.count(),
        }
    ]

    context = {
        "active_page": "potential_stock",
        "stoch_result": stoch_result,
        "to_calculate": to_calculate,
    }
    return render(request, "potential_stock/base_page.html", context)


# ============================= Short Term page ==============================
@login_required(login_url="/accounts/login/")
def short_term_page(request):
    ha_wma_cross_yesterday = StochHourlyTrend.objects.filter(ha_wma_cross_last_hour=True, ha_wma_top=True).order_by(
        "d_value"
    )
    ha_cross_yesterday = StochHourlyTrend.objects.filter(ha_cross_last_hour=True, ha_positive=True).order_by("d_value")
    to_calculate = StochHourlyTrend.objects.filter(date=datetime.today()).count()
    stoch_result = [
        {
            "title": "HA WMA Cross Last hour",
            "reference": "ha_top",
            "icon": "fa fa-solid fa-level-up",
            "stoch_value": list(ha_wma_cross_yesterday.values()),
            "stoch_count": ha_wma_cross_yesterday.count(),
        },
        {
            "title": "HA Cross Last hour",
            "reference": "ha_top",
            "icon": "fa fa-solid fa-level-up",
            "stoch_value": list(ha_cross_yesterday.values()),
            "stoch_count": ha_cross_yesterday.count(),
        },
    ]

    context = {
        "active_page": "short_term",
        "stoch_result": stoch_result,
        "to_calculate": to_calculate,
    }
    return render(request, "short_term/base_page.html", context)


# ======================================================================================

