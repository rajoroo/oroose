# Generated by Django 4.0.7 on 2022-10-17 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bengaluru', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fivehundred',
            name='rank',
            field=models.IntegerField(blank=True, null=True, verbose_name='Rank'),
        ),
    ]