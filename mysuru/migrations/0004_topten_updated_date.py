# Generated by Django 4.0.7 on 2023-03-15 11:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mysuru', '0003_remove_topten_macd_status_remove_topten_today_macd_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topten',
            name='updated_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Updated Date'),
            preserve_default=False,
        ),
    ]
