import io
import pandas as pd
from mysuru.models import StockData


class StockCollection:
    """Stock collection create, fetch, and reset stock"""

    def create(self, csv_file):
        """Create stock data"""
        StockData.objects.all().delete()
        csv_data = io.StringIO(csv_file.read().decode("utf-8"))
        df = pd.read_csv(csv_data)
        stocks = [
            StockData(
                symbol=row["symbol"],
            )
            for index, row in df.iterrows()
        ]
        StockData.objects.bulk_create(stocks)

    def fetch_smart_token(self):
        """Add smart token to stock data"""
        recs = StockData.objects.all()
        for rec in recs:
            rec.get_smart_token()

        StockData.objects.filter(smart_token__isnull=True, smart_token_fetched=True).delete()
        return True

    def fetch(self, data_type):
        """Fetch stock data"""
        filter_params = {f"is_{data_type}_fetched": False}
        recs = StockData.objects.filter(**filter_params)[:500]
        for rec in recs:
            rec.generate_trend_value(data_type=data_type)

        return True

    def reset(self, data_type):
        """Reset stock data"""
        filter_params = {f"is_{data_type}_fetched": True}
        update_params = {f"is_{data_type}_fetched": False}
        recs = StockData.objects.filter(**filter_params)
        recs.update(**update_params)
        return True
