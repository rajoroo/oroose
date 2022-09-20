# Generated by Django 4.0.7 on 2022-09-20 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bengaluru', '0006_fhzero'),
    ]

    operations = [
        migrations.AddField(
            model_name='fhzero',
            name='status',
            field=models.CharField(choices=[('TO_BUY', 'To Buy'), ('PURCHASED', 'Purchased'), ('TO_SELL', 'To Sell'), ('SOLD', 'Sold')], default='SOLD', max_length=10, verbose_name='Status'),
            preserve_default=False,
        ),
    ]
