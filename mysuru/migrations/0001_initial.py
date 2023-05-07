# Generated by Django 4.2.1 on 2023-05-07 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MacdTrend",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="Date")),
                ("updated_date", models.DateField(blank=True, null=True, verbose_name="Updated Date")),
                ("symbol", models.CharField(max_length=200, verbose_name="Symbol")),
                ("smart_token", models.CharField(blank=True, max_length=50, null=True, verbose_name="Smart Token")),
                ("identifier", models.CharField(max_length=200, verbose_name="Identifier")),
                ("company_name", models.CharField(max_length=500, verbose_name="Company Name")),
                ("isin", models.CharField(max_length=100, verbose_name="Isin")),
                ("price", models.FloatField(verbose_name="Price")),
                ("percentage_change", models.FloatField(verbose_name="Percentage")),
                ("ema_200", models.FloatField(blank=True, null=True, verbose_name="Ema200")),
                ("ema_50", models.FloatField(blank=True, null=True, verbose_name="Ema50")),
                ("last_close", models.FloatField(blank=True, null=True, verbose_name="Last Close")),
                ("day_1_status", models.BooleanField(default=False, verbose_name="Day 1")),
                ("day_2_status", models.BooleanField(default=False, verbose_name="Day 2")),
                ("ema_200_percentage", models.FloatField(default=0.0, verbose_name="Ema 200 Percentage")),
                ("trend_status", models.BooleanField(default=False, verbose_name="Trend Status")),
            ],
            options={
                "ordering": ["-date", "symbol"],
            },
        ),
        migrations.CreateModel(
            name="PriceAction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("symbol", models.CharField(max_length=200, verbose_name="Symbol")),
                ("smart_token", models.CharField(blank=True, max_length=50, null=True, verbose_name="Smart Token")),
                ("identifier", models.CharField(max_length=200, verbose_name="Identifier")),
                ("company_name", models.CharField(max_length=500, verbose_name="Company Name")),
                ("price_data", models.JSONField(blank=True, null=True, verbose_name="Price Data")),
            ],
            options={
                "ordering": ["symbol"],
            },
        ),
        migrations.AddConstraint(
            model_name="priceaction",
            constraint=models.UniqueConstraint(fields=("symbol",), name="mysuru_priceaction_price_action"),
        ),
        migrations.AddConstraint(
            model_name="macdtrend",
            constraint=models.UniqueConstraint(fields=("date", "symbol"), name="mysuru_macdtrend_unique_macd_trend"),
        ),
    ]
