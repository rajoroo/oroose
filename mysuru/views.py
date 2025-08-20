from mysuru.stock_collection import StockCollection
from django.views.decorators.csrf import csrf_exempt
from home.forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect
from django.template.loader import render_to_string
from django.urls import reverse


@csrf_exempt
def stock_collection_upload(request):
    """Upload and create stock data"""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            trend_obj = StockCollection()
            trend_obj.create(request.FILES["file"])
            return HttpResponseRedirect(reverse("configuration"))
    else:
        form = UploadFileForm()
    rendered = render_to_string("configuration/stock_file_upload.html", {"form": form, "title": "Upload Stocks"})
    response = HttpResponse(rendered)
    return response


def stock_collection_fetch_smart_token(request):
    """Add smart token to stock data"""
    trend_obj = StockCollection()
    trend_obj.fetch_smart_token()
    return redirect("configuration")


def stock_collection_fetch(request, name):
    """Fetch stock data"""
    trend_obj = StockCollection()
    trend_obj.fetch(name)
    return redirect("configuration")


def stock_collection_reset(request, name):
    """Reset stock data"""
    trend_obj = StockCollection()
    trend_obj.reset(name)
    return redirect("configuration")

