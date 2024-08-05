from django import forms
from mysuru.models import StockData

TradingStatus = [
    ('up', 'UP'),
    ('dn', 'DOWN'),
]


class TradingForm(forms.Form):
    symbol = forms.ModelChoiceField(
        queryset=StockData.objects.all(),
        widget=forms.Select(attrs={"class": "form-select resize-select"})
    )
    trading_status = forms.ChoiceField(
        choices=TradingStatus,
        widget=forms.Select(attrs={"class": "form-select resize-select"})
    )
