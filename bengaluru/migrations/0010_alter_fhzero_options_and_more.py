# Generated by Django 4.0.7 on 2022-09-21 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bengaluru', '0009_remove_fivehundred_sequence_alter_fhzero_buy_price_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fhzero',
            options={'ordering': ['-date', 'symbol']},
        ),
        migrations.AddConstraint(
            model_name='fhzero',
            constraint=models.UniqueConstraint(fields=('date', 'tag'), name='bengaluru_fhzero_unique_tag'),
        ),
    ]
