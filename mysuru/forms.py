from django import forms
from mysuru.models import StockData


class TradingForm(forms.Form):
    symbol = forms.ModelChoiceField(
        queryset=StockData.objects.all(), widget=forms.Select(attrs={"class": "form-select resize-select"})
    )
