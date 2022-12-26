from django.forms import ModelForm

from bengaluru.models import FhZeroDownTrend, FhZeroUpTrend


# Create the form class.
class FhZeroUpTrendForm(ModelForm):
    class Meta:
        model = FhZeroUpTrend
        fields = [
            "date",
            "time",
            "five_hundred",
            "symbol",
            "isin",
            "status",
            "buy_id",
            "sell_id",
            "quantity",
            "last_price",
            "buy_price",
            "sell_price",
            "current_price",
            "error",
            "error_message",
        ]


class FhZeroDownTrendForm(ModelForm):
    class Meta:
        model = FhZeroDownTrend
        fields = [
            "date",
            "time",
            "five_hundred",
            "symbol",
            "isin",
            "status",
            "buy_id",
            "sell_id",
            "quantity",
            "last_price",
            "buy_price",
            "sell_price",
            "current_price",
            "error",
            "error_message",
        ]
