from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import FiveHundred
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from core.stocks import NseStocks
from core.pas import first_five
from django.conf import settings


@login_required(login_url='/accounts/login/')
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, 'bengaluru/base.html', context)


def load_nifty_500_nse(request):
    print(settings.NSE_EQUITY_INDEX)
    print(settings.NIFTY_500_PAYLOAD)
    obj = NseStocks(url=settings.NSE_EQUITY_INDEX, payload=settings.NIFTY_500_PAYLOAD)
    k = obj.get_data()
    print(k)
    first_five(value=k)
    return HttpResponse(status=200)


def load_five_hundred(request):
    # obj = FiveHundred.objects.all()
    obj = FiveHundred.objects.filter(date=datetime.today())
    context = {"items": list(obj.values())}

    return render(request, 'bengaluru/load-500.html', context=context)
