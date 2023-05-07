from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from core.models import ParameterConfig
from core.smart_util import SmartTool
from core.tools import get_param_config_tag, handle_config_file, save_param_config_tag
from home.forms import UploadFileForm


@login_required(login_url="/accounts/login/")
def home_page(request):
    context = {"active_page": "home"}
    return render(request, "base/home.html", context)


@login_required(login_url="/accounts/login/")
def configuration_page(request):
    configs = ParameterConfig.objects.all()
    context = {"active_page": "configuration", "configs": configs}
    return render(request, "configuration/configure_settings.html", context=context)


@csrf_exempt
def upload_config_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_config_file(request.FILES["file"])
            return HttpResponseRedirect(reverse("configuration"))
    else:
        form = UploadFileForm()
    rendered = render_to_string("configuration/file_upload.html", {"form": form, "title": "Upload Configs"})
    response = HttpResponse(rendered)
    return response


def generate_smart_token(request):
    """Pull the five hundred data from stock api"""
    # SMART Token
    config = get_param_config_tag(tag="SMART_HISTORY")

    obj = SmartTool(
        api_key=config["api_key"],
        client_code=config["client_code"],
        password=config["password"],
        totp=config["totp"],
    )
    params = obj.generate_token()
    save_param_config_tag(params=params, tag="SMART_HISTORY")
    return redirect("configuration")


def reset_configuration(request):
    """Reset configurations"""
    ParameterConfig.objects.all().delete()
    return redirect("configuration")
