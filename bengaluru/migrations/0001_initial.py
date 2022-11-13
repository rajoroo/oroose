# Generated by Django 4.0.7 on 2022-11-13 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FhZeroUpTrend",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="Date")),
                ("time", models.DateTimeField(verbose_name="Time")),
                ("updated_date", models.DateTimeField(auto_now_add=True, verbose_name="Updated Date")),
                ("symbol", models.CharField(max_length=200, verbose_name="Symbol")),
                ("isin", models.CharField(max_length=100, verbose_name="Isin")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("TO_BUY", "To Buy"),
                            ("PURCHASED", "Purchased"),
                            ("TO_SELL", "To Sell"),
                            ("SOLD", "Sold"),
                        ],
                        max_length=10,
                        verbose_name="Status",
                    ),
                ),
                ("buy_id", models.CharField(blank=True, max_length=100, null=True, verbose_name="Buy ID")),
                ("sell_id", models.CharField(blank=True, max_length=100, null=True, verbose_name="Sell ID")),
                ("quantity", models.IntegerField(verbose_name="Quantity")),
                ("last_price", models.FloatField(verbose_name="Last Price")),
                ("buy_price", models.FloatField(default=0.0, verbose_name="Buy Price")),
                ("sell_price", models.FloatField(default=0.0, verbose_name="Sell Price")),
                ("current_price", models.FloatField(default=0.0, verbose_name="Current Price")),
                ("error", models.BooleanField(default=False, verbose_name="Error")),
                ("error_message", models.TextField(blank=True, null=True, verbose_name="Error Message")),
            ],
            options={
                "ordering": ["symbol"],
            },
        ),
        migrations.CreateModel(
            name="FiveHundred",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="Date")),
                ("time", models.DateTimeField(verbose_name="Time")),
                ("rank", models.IntegerField(verbose_name="Rank")),
                ("symbol", models.CharField(max_length=200, verbose_name="Symbol")),
                ("identifier", models.CharField(max_length=200, verbose_name="Identifier")),
                ("company_name", models.CharField(max_length=500, verbose_name="Company Name")),
                ("isin", models.CharField(max_length=100, verbose_name="Isin")),
                ("last_price", models.FloatField(verbose_name="Price")),
                ("percentage_change", models.FloatField(verbose_name="Percentage")),
            ],
            options={
                "ordering": ["-date", "rank"],
            },
        ),
        migrations.AddConstraint(
            model_name="fivehundred",
            constraint=models.UniqueConstraint(
                fields=("date", "symbol"), name="bengaluru_fivehundred_unique_five_hundred"
            ),
        ),
        migrations.AddField(
            model_name="fhzerouptrend",
            name="five_hundred",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="bengaluru.fivehundred",
                verbose_name="Five Hundred",
            ),
        ),
    ]
