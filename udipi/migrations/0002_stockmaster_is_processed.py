# Generated by Django 4.0.7 on 2023-01-23 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udipi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmaster',
            name='is_processed',
            field=models.BooleanField(default=False, verbose_name='Is Processed'),
        ),
    ]
