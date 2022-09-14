from django.contrib.auth.decorators import login_required
from core.models import ConfigureSettings
from django.shortcuts import render
from django.http import HttpResponse


@login_required(login_url='/accounts/login/')
def home(request):
    context = {"active_page": "home"}
    return render(request, 'base/home.html', context)


@login_required(login_url='/accounts/login/')
def load_configuration(request):
    obj = ConfigureSettings.objects.all()
    context = {
        "items": list(obj.values()),
        "active_page": "configuration"
    }
    return render(request, 'base/configure_settings.html', context=context)


@login_required(login_url='/accounts/login/')
def config_update(request, config_id):
    status = request.GET.get('status', 'false')
    obj = ConfigureSettings.objects.get(id=config_id)
    obj.status = True if status == "true" else False
    obj.save()
    return HttpResponse(status=200)
