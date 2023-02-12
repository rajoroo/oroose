# Generated by Django 4.0.7 on 2023-02-12 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stockwatch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FhZeroUpTrend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('created_date', models.DateTimeField(verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now_add=True, verbose_name='Updated Date')),
                ('symbol', models.CharField(max_length=200, verbose_name='Symbol')),
                ('isin', models.CharField(max_length=100, verbose_name='Isin')),
                ('status', models.CharField(choices=[('TO_BUY', 'To Buy'), ('PURCHASED', 'Purchased'), ('TO_SELL', 'To Sell'), ('SOLD', 'Sold')], max_length=10, verbose_name='Status')),
                ('buy_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Buy ID')),
                ('sell_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Sell ID')),
                ('rank', models.IntegerField(verbose_name='Rank')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('last_price', models.FloatField(verbose_name='Last Price')),
                ('buy_price', models.FloatField(default=0.0, verbose_name='Buy Price')),
                ('sell_price', models.FloatField(default=0.0, verbose_name='Sell Price')),
                ('current_price', models.FloatField(default=0.0, verbose_name='Current Price')),
                ('high_price', models.FloatField(default=0.0, verbose_name='Current Price')),
                ('trigger_price', models.FloatField(default=0.0, verbose_name='Current Price')),
                ('pl_price', models.FloatField(default=0.0, verbose_name='PL Price')),
                ('error', models.BooleanField(default=False, verbose_name='Error')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='Error Message')),
                ('pl_status', models.CharField(choices=[('WR', 'Winner'), ('RR', 'Runner'), ('IP', 'In-Progress')], default='IP', max_length=2)),
                ('five_hundred', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stockwatch.fivehundred', verbose_name='Five Hundred')),
            ],
            options={
                'ordering': ['symbol'],
            },
        ),
    ]
