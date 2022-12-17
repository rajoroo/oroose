from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import reverse

from bengaluru.models import FhZeroUpTrend, FhZeroStatus
from django.views.generic.edit import UpdateView
from django.shortcuts import render


# Uptrend
@login_required(login_url="/accounts/login/")
def bengaluru_page(request):
    context = {"active_page": "bengaluru"}
    return render(request, "bengaluru/base_page.html", context)


def load_fhz_uptrend_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = (
        FhZeroUpTrend.objects.filter(
            date=datetime.today(),
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
            error=False,
        ).annotate(current_pl=F("quantity") * (F("current_price") - F("buy_price")))
    ).order_by("-updated_date")

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "bengaluru/load_fh_zero_view.html", context=context)


def load_fhz_uptrend_error_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZeroUpTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
        error=True,
    ).annotate(profit_loss=F("quantity") * (F("sell_price") - F("buy_price")))

    context = {
        "items": list(fhz.values()),
    }
    return render(request, "bengaluru/load_fh_zero_error_view.html", context=context)


def load_fhz_uptrend_sold_view(request):
    """Load five hundred zero objects display in table view"""
    fhz = FhZeroUpTrend.objects.filter(date=datetime.today(), status=FhZeroStatus.SOLD).annotate(
        profit_loss=F("quantity") * (F("sell_price") - F("buy_price"))
    )

    context = {"items": list(fhz.values()), "realized_amount": fhz.aggregate(Sum("profit_loss"))["profit_loss__sum"]}
    return render(request, "bengaluru/load_fh_zero_sold_view.html", context=context)


class EditFhzUptrend(UpdateView):
    model = FhZeroUpTrend
    template_name = "trend_view/fhz_uptrend.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("fhz_uptrend_record", kwargs={"pk": self.object.id})
