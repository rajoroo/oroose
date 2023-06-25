# Generated by Django 4.2.1 on 2023-06-25 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mysuru", "0002_stochtrend_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StochDailyTrend",
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
                ("stoch_status", models.BooleanField(default=False, verbose_name="Stoch Status")),
                ("stoch_positive_trend", models.BooleanField(default=False, verbose_name="Stoch Positive Trend")),
                ("ema_200_percentage", models.FloatField(default=0.0, verbose_name="Ema 200 Percentage")),
                ("trend_status", models.BooleanField(default=False, verbose_name="Trend Status")),
            ],
            options={
                "ordering": ["-date", "symbol"],
            },
        ),
        migrations.CreateModel(
            name="StochWeeklyTrend",
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
                ("stoch_status", models.BooleanField(default=False, verbose_name="Stoch Status")),
                ("stoch_positive_trend", models.BooleanField(default=False, verbose_name="Stoch Positive Trend")),
                ("ema_200_percentage", models.FloatField(default=0.0, verbose_name="Ema 200 Percentage")),
                ("trend_status", models.BooleanField(default=False, verbose_name="Trend Status")),
            ],
            options={
                "ordering": ["-date", "symbol"],
            },
        ),
        migrations.DeleteModel(
            name="StochTrend",
        ),
        migrations.AddConstraint(
            model_name="stochweeklytrend",
            constraint=models.UniqueConstraint(
                fields=("date", "symbol"), name="mysuru_stochweeklytrend_unique_stoch_trend"
            ),
        ),
        migrations.AddConstraint(
            model_name="stochdailytrend",
            constraint=models.UniqueConstraint(
                fields=("date", "symbol"), name="mysuru_stochdailytrend_unique_stoch_trend"
            ),
        ),
    ]
