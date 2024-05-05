from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import F

from mysuru.fetch_trend import get_model_object, FetchTrend
from mysuru.models import HourlyTrend, WeeklyTrend, DailyTrend


# =========================================Trend==========================================
@login_required(login_url="/accounts/login/")
def trend_page(request, name):
    """Trend page for display Hourly/ Daily/ Weekly"""
    model_obj = get_model_object(name)
    total_stock = model_obj.objects.all().count()
    all_stock_list = model_obj.objects.all()
    to_calculate = model_obj.objects.filter(is_fetched=False).count()
    ha_cross_ma_20 = model_obj.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open_0__lt=F("ha_close_0"),
        ema_20__lt=F("ha_close_0"),
        ema_20__gt=F("ha_open_0"),
    )
    items = [
        {
            "title": "All Stocks",
            "stocks": all_stock_list,
            "count": all_stock_list.count(),
        },
        {
            "title": "20 Moving average crossed",
            "description": """Helsinki-asli cross the 20 moving average""",
            "stocks": ha_cross_ma_20,
            "count": ha_cross_ma_20.count(),
        },
    ]
    context = {
        "page_title": name.upper(),
        "active_page": "trend_page",
        "active_path": name,
        "items": items,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "trend/base_page.html", context)


def trend_page_load_live(request, name):
    """
    Load live stocks
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.fetch_live_stocks()
    trend_obj.create_trend()
    return redirect("trend_page", name=name)


def trend_page_load_bhav(request, name):
    """
    Load bhav copy stocks
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.fetch_bhav_copy()
    trend_obj.create_trend()
    return redirect("trend_page", name=name)


def trend_page_upload(request, name):
    pass


def trend_page_load_futures(request, name):
    """
    Load futures stocks
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.fetch_futures_stocks()
    trend_obj.create_trend()
    return redirect("trend_page", name=name)


def trend_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.fetch_trend_value()
    return redirect("trend_page", name=name)


def trend_page_reset(request, name):
    """
    Reset trend model to fetch form the API
    Parameters:
        name - model name string representation
    """
    model_obj = get_model_object(name)
    trend_obj = FetchTrend(model_obj)
    trend_obj.reset_fetched()
    return redirect("trend_page", name=name)


def potential_page(request):
    """
    Potential page
    WeeklyTrend with
        Uptrend
        - moving average 20 > 200
        - moving average 20 > 50
        Heikin-ashi
        - candle is green
        - candle > moving average 20
    """
    total_stock = WeeklyTrend.objects.all().count()
    to_calculate = WeeklyTrend.objects.filter(is_fetched=False).count()
    potential_stocks_cross = WeeklyTrend.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open_0__lt=F("ha_close_0"),
        ema_20__lt=F("ha_close_0"),
        ema_20__gt=F("ha_open_0"),
    )
    potential_stocks_rsi = WeeklyTrend.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open_0__lt=F("ha_close_0"),
        ema_20__lt=F("ha_open_0"),
        rsi_0__gt=60
    ).order_by("rsi")
    potential_stocks_stoch = WeeklyTrend.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open_0__lt=F("ha_close_0"),
        ema_20__lt=F("ha_open_0"),
        stoch_black_0__gt=F("stoch_red_0"),
        stoch_black_0__gte=20,
        stoch_black_0__lte=80,
    ).order_by("stoch_black")
    items = [
        {
            "title": "Potential Stocks Crossed",
            "stocks": potential_stocks_cross,
            "count": potential_stocks_cross.count(),
        },
        {
            "title": "Potential Stocks RSI",
            "stocks": potential_stocks_rsi,
            "count": potential_stocks_rsi.count(),
        },
        {
            "title": "Potential Stocks Stoch",
            "stocks": potential_stocks_stoch,
            "count": potential_stocks_stoch.count(),
        },
    ]
    context = {
        "page_title": "POTENTIAL",
        "active_page": "potential_page",
        "active_path": None,
        "items": items,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "others/base_page.html", context)


def short_term_page(request):
    """
    Short term page
    HourlyTrend with
        Uptrend
        - moving average 20 > 200
        - moving average 20 > 50
        Heikin-ashi
        - candle is green
        - moving average 20 is crossing candle
    """
    potential_stocks_list = WeeklyTrend.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open__lt=F("ha_close"),
        ema_20__lt=F("ha_open"),
    ).values_list("symbol")
    short_term_cross = DailyTrend.objects.filter(
        is_fetched=True,
        symbol__in=potential_stocks_list,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open__lt=F("ha_close"),
        ema_20__lt=F("ha_close"),
        ema_20__gt=F("ha_open"),
    )
    short_term_rsi = DailyTrend.objects.filter(
        is_fetched=True,
        symbol__in=potential_stocks_list,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open__lt=F("ha_close"),
        ema_20__lt=F("ha_open"),
        rsi__gt=60
    ).order_by("rsi")
    short_term_stoch = DailyTrend.objects.filter(
        is_fetched=True,
        symbol__in=potential_stocks_list,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open__lt=F("ha_close"),
        ema_20__lt=F("ha_open"),
        stoch_black__gt=F("stoch_red"),
        stoch_black__gte=20,
        # stoch_black__lte=80,
    ).order_by("stoch_black")
    total_stock = DailyTrend.objects.all().count()
    to_calculate = DailyTrend.objects.filter(is_fetched=False).count()
    items = [
        {
            "title": "Short Term Crossed",
            "stocks": short_term_cross,
            "count": short_term_cross.count(),
        },
        {
            "title": "Short Term RSI",
            "stocks": short_term_rsi,
            "count": short_term_rsi.count(),
        },
        {
            "title": "Short Terms Stoch",
            "stocks": short_term_stoch,
            "count": short_term_stoch.count(),
        },
    ]
    context = {
        "page_title": "SHORT TERM",
        "active_page": "short_term_page",
        "active_path": None,
        "items": items,
        "to_calculate": to_calculate,
        "total_stock": total_stock,
    }
    return render(request, "others/base_page.html", context)


def copy_eligible_stocks(request):
    """Filter weekly trend and copy eligible stocks to hourly"""
    recs = WeeklyTrend.objects.filter(
        is_fetched=True,
        ema_200__lt=F("ema_20"),
        ema_50__lt=F("ema_20"),
        ha_open__lt=F("ha_close"),
        ema_20__lt=F("ha_open"),
    )
    trend_obj = FetchTrend(HourlyTrend)
    trend_obj.stock_data = [{"symbol": rec.symbol, "company_name": rec.company_name} for rec in recs]
    trend_obj.create_trend()
    # HourlyTrend.objects.all().delete()
    # create_list = [HourlyTrend(symbol=rec.symbol, company_name=rec.company_name) for rec in recs]
    # HourlyTrend.objects.bulk_create(create_list)
    return redirect("trend_page", name="hourly")
