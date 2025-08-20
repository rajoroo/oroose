import io
import pandas as pd
from mysuru.models import StockData


class FetchTrend:
    def create_trend(self, csv_file):
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

    def fetch_trend_value(self, data_type):
        """Fetch trend value"""
        filter_params = {f"is_{data_type}_fetched": False}
        recs = StockData.objects.filter(**filter_params)[:500]
        for rec in recs:
            rec.generate_trend_value(data_type=data_type)

        return True

    def trend_reset(self, data_type):
        """Fetch potential trend value"""
        filter_params = {f"is_{data_type}_fetched": True}
        update_params = {f"is_{data_type}_fetched": False}
        recs = StockData.objects.filter(**filter_params)
        recs.update(**update_params)
        return True

