# Generated by Django 4.2.1 on 2024-02-04 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mysuru", "0006_stochdailytrend_heikin_ashi_top"),
    ]

    operations = [
        migrations.AddField(
            model_name="stochdailytrend",
            name="heikin_ashi_crossed_yesterday",
            field=models.BooleanField(default=False, verbose_name="Heikin-Ashi Crossed Yesterday"),
        ),
    ]