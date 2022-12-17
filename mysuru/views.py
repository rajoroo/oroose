from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import reverse

from mysuru.models import FhZeroDownTrend
from core.choice import FhZeroStatus
from mysuru.down_trend import downtrend_panic_pull
from django.views.generic.edit import UpdateView

from django.shortcuts import render


# Downtrend
@login_required(login_url="/accounts/login/")
def mysuru_page(request):
    context = {"active_page": "mysuru"}
    return render(request, "mysuru/base_page.html", context)


def load_fhz_downtrend_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = (
        FhZeroDownTrend.objects.filter(
            date=datetime.today(),
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.SOLD, FhZeroStatus.TO_SELL],
            error=False,
        ).annotate(current_pl=F("quantity") * (F("sell_price") - F("current_price")))
    ).order_by("-updated_date")

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "mysuru/load_fh_zero_view.html", context=context)


def load_fhz_downtrend_error_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZeroDownTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.SOLD, FhZeroStatus.TO_SELL],
        error=True,
    ).annotate(profit_loss=F("quantity") * (F("sell_price") - F("buy_price")))

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "mysuru/load_fh_zero_error_view.html", context=context)


def load_fhz_downtrend_purc_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZeroDownTrend.objects.filter(date=datetime.today(), status=FhZeroStatus.PURCHASED).annotate(
        profit_loss=F("quantity") * (F("sell_price") - F("buy_price"))
    )

    context = {"items": list(fhz.values()), "realized_amount": fhz.aggregate(Sum("profit_loss"))["profit_loss__sum"]}
    return render(request, "mysuru/load_fh_zero_sold_view.html", context=context)


def trigger_downtrend_panic_pull(request):
    downtrend_panic_pull()
    return HttpResponse(status=200)


class EditFhzDowntrend(UpdateView):
    model = FhZeroDownTrend
    template_name = "trend_view/fhz_downtrend.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("fhz_downtrend_record", kwargs={"pk": self.object.id})
