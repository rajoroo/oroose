# Generated by Django 4.2.1 on 2024-02-19 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mysuru", "0011_remove_stochhourlytrend_ha_cross_yesterday_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stochdailytrend",
            name="rsi",
            field=models.FloatField(default=0.0, verbose_name="D value"),
        ),
        migrations.AddField(
            model_name="stochhourlytrend",
            name="rsi",
            field=models.FloatField(default=0.0, verbose_name="D value"),
        ),
    ]
