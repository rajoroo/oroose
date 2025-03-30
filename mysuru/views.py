from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import F, Q, Case, When, Value, BooleanField

from mysuru.forms import TradingForm
from mysuru.fetch_trend import FetchTrend
from mysuru.models import StockData
from datetime import datetime
from mysuru.task import trading_m5_fetch
from django_q.tasks import schedule
from django_q.models import Schedule
import arrow


@login_required(login_url="/accounts/login/")
def trading_negative_page(request):
    """Trend page for display potential"""
    annotate_params = {
        "m5_1": Case(
            When(m5_ha_open_1__lt=F("m5_ha_close_1"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m5_2": Case(
            When(m5_ha_open_2__lt=F("m5_ha_close_2"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m5_3": Case(
            When(m5_ha_open_3__lt=F("m5_ha_close_3"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        "m5_ha_cross_1": Case(
            When(m5_ema_20_1__lt=F("m5_ha_close_1"), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
    }
    stock_list = StockData.objects.filter(is_trading=True).annotate(**annotate_params)
    latest_record = StockData.objects.latest("trading_updated_at")
    if request.method == "POST":
        form = TradingForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data["symbol"]
            trading_status = form.cleaned_data["trading_status"]
            stock_data = StockData.objects.get(symbol=symbol)
            if "_add" in request.POST:
                stock_data.is_trading = True
                stock_data.trading_status = trading_status
            elif "_remove" in request.POST:
                stock_data.is_trading = False
            stock_data.save()
            return redirect("trading")
    else:
        form = TradingForm()
    context = {
        "title": "Monitoring",
        "form": form,
        "stocks": stock_list,
        "trading_updated_at": latest_record.trading_updated_at if latest_record else "",
    }
    return render(request, "stock/trading_negative_page.html", context)


def trend_page_load_live(request):
    """
    Load live stocks
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_live_stocks()
    trend_obj.create_trend()
    return redirect("configuration")


def trend_page_load_bhav(request):
    """
    Load bhav copy stocks
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_bhav_copy()
    trend_obj.create_trend()
    return redirect("configuration")


def trend_page_load_m15_short(request):
    trend_obj = FetchTrend()
    trend_obj.fetch_trend_m15_short_value("m15")
    return redirect("configuration")


def trend_page_upload(request):
    pass


def trend_page_load_futures(request):
    """
    Load futures stocks
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    # trend_obj.fetch_futures_stocks()
    trend_obj.fetch_futures_stocks_smart()
    trend_obj.create_trend()
    return redirect("configuration")


def trend_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_trend_value(name)
    return redirect("configuration")


def potential_trend_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_potential_trend_value(name)
    return redirect("configuration")


def trading_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trading_m5_fetch(name)
    return redirect("configuration")


def trend_page_reset_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.trend_reset(name)
    return redirect("configuration")


def schedule_trading_start(request):
    # schedule("mysuru.task.trading_m5_fetch", "m5", schedule_type=Schedule.MINUTES, minutes=5)
    schedule("mysuru.task.trading_m5_sensitive_fetch", "hr", schedule_type=Schedule.MINUTES, minutes=5)
    return redirect("configuration")
