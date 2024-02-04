# Generated by Django 4.2.1 on 2024-02-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mysuru", "0004_alter_stochweeklytrend_company_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stochdailytrend",
            name="heikin_ashi_crossed",
            field=models.BooleanField(default=False, verbose_name="Heikin-Ashi Crossed"),
        ),
    ]
