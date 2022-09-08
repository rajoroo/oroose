from django.shortcuts import render
from django.http import JsonResponse
from .models import FiveHundred
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def docs(request):
    context = {"active_page": "docs"}
    return render(request, 'bengaluru/docs.html', context)


def load_five_hundred(request):
    obj = FiveHundred.objects.all()
    context = {"items": list(obj.values())}

    return render(request, 'bengaluru/load-500.html', context=context)
