# Generated by Django 4.1.1 on 2022-09-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bengaluru', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fivehundred',
            old_name='price',
            new_name='last_price',
        ),
        migrations.RenameField(
            model_name='fivehundred',
            old_name='isbin',
            new_name='isin',
        ),
        migrations.AddField(
            model_name='fivehundred',
            name='percentage_change',
            field=models.FloatField(default=1, verbose_name='Percentage'),
            preserve_default=False,
        ),
    ]