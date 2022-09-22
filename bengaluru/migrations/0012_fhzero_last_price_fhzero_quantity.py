# Generated by Django 4.0.7 on 2022-09-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bengaluru', '0011_rename_fh_id_fhzero_five_hundred'),
    ]

    operations = [
        migrations.AddField(
            model_name='fhzero',
            name='last_price',
            field=models.FloatField(default=0.0, verbose_name='Last Price'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fhzero',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
    ]
