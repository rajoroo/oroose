# Generated by Django 4.0.7 on 2022-11-28 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bengaluru', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fivehundred',
            name='highest_rank',
            field=models.IntegerField(blank=True, null=True, verbose_name='Highest Rank'),
        ),
        migrations.AddField(
            model_name='fivehundred',
            name='lowest_rank',
            field=models.IntegerField(blank=True, null=True, verbose_name='Lowest Rank'),
        ),
        migrations.AddField(
            model_name='fivehundred',
            name='previous_rank',
            field=models.IntegerField(blank=True, null=True, verbose_name='Previous Rank'),
        ),
    ]