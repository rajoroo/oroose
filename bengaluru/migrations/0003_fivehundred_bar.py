# Generated by Django 4.0.7 on 2022-12-07 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bengaluru', '0002_fivehundred_highest_rank_fivehundred_lowest_rank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fivehundred',
            name='bar',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Bar'),
        ),
    ]
