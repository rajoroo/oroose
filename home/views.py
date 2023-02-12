from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import HttpResponse, render, redirect
from django.template import Template, Context
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt

from core.configuration import parameter_store
from core.models import DataLog, ParameterSettings, ParameterConfig

from django.http import HttpResponseRedirect
from home.forms import UploadFileForm
from core.tools import handle_config_file, get_param_config_tag, save_param_config_tag
from core.smart_util import SmartTool
from django.urls import reverse


@login_required(login_url="/accounts/login/")
def home_page(request):
    context = {"active_page": "home"}
    return render(request, "base/home.html", context)


@login_required(login_url="/accounts/login/")
def configuration_page(request):
    param_settings = ParameterSettings.objects.all()
    configs = ParameterConfig.objects.all()
    context = {"param_configs": parameter_store, "param_settings": param_settings, "active_page": "configuration", "configs": configs}
    return render(request, "configuration/configure_settings.html", context=context)


@login_required(login_url="/accounts/login/")
def data_log_page(request):
    obj = DataLog.objects.filter(date=datetime.today())[:25]
    obj.annotate(seconds_diff=F("end_time") - F("start_time"))

    context = {"items": list(obj.values()), "active_page": "data_log"}
    return render(request, "base/data_log_view.html", context=context)


def params_update(request, config_id):
    status = request.GET.get("status", "false")
    obj = ParameterSettings.objects.get(id=config_id)
    obj.status = True if status == "true" else False
    obj.save()
    return HttpResponse(status=200)


@csrf_exempt
def upload_config_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_config_file(request.FILES['file'])
            return HttpResponseRedirect(reverse("configuration"))
    else:
        form = UploadFileForm()
    rendered = render_to_string('configuration/file_upload.html', {'form': form, "title": "Upload Configs"})
    response = HttpResponse(rendered)
    return response


def generate_smart_token(request):
    """Pull the five hundred data from stock api"""

    config = get_param_config_tag(tag="SMART")

    obj = SmartTool(
        api_key=config["api_key"],
        client_code=config["client_code"],
        password=config["password"],
        totp=config["totp"],
    )
    params = obj.generate_token()
    save_param_config_tag(params=params, tag="SMART")
    return HttpResponse(status=200)
