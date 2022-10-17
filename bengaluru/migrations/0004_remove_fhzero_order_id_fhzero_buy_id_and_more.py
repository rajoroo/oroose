# Generated by Django 4.0.7 on 2022-10-17 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bengaluru', '0003_alter_fivehundred_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fhzero',
            name='order_id',
        ),
        migrations.AddField(
            model_name='fhzero',
            name='buy_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Buy ID'),
        ),
        migrations.AddField(
            model_name='fhzero',
            name='stop_loss_price',
            field=models.FloatField(default=0.0, verbose_name='Buy Price'),
        ),
    ]