# Generated by Django 4.2.1 on 2024-02-04 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mysuru", "0005_stochdailytrend_heikin_ashi_crossed"),
    ]

    operations = [
        migrations.AddField(
            model_name="stochdailytrend",
            name="heikin_ashi_top",
            field=models.BooleanField(default=False, verbose_name="Heikin-Ashi Top"),
        ),
    ]
