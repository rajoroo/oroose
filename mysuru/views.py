from mysuru.fetch_trend import FetchTrend
from django.views.decorators.csrf import csrf_exempt
from home.forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect
from django.template.loader import render_to_string
from django.urls import reverse


@csrf_exempt
def trend_page_upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            trend_obj = FetchTrend()
            trend_obj.create_trend(request.FILES["file"])
            return HttpResponseRedirect(reverse("configuration"))
    else:
        form = UploadFileForm()
    rendered = render_to_string("configuration/stock_file_upload.html", {"form": form, "title": "Upload Stocks"})
    response = HttpResponse(rendered)
    return response


def trend_page_fetch(request, name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_trend_value(name)
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

