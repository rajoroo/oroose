# Generated by Django 4.0.7 on 2022-12-19 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stockwatch", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="company_name",
        ),
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="identifier",
        ),
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="isin",
        ),
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="last_price",
        ),
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="percentage_change",
        ),
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="rank",
        ),
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="symbol",
        ),
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="time",
        ),
        migrations.RemoveField(
            model_name="stockwatchfh",
            name="uid",
        ),
        migrations.AddField(
            model_name="stockwatchfh",
            name="stock_data",
            field=models.JSONField(blank=True, null=True, verbose_name="Stock Data"),
        ),
    ]