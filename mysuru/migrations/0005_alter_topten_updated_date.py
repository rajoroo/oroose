# Generated by Django 4.0.7 on 2023-03-15 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mysuru", "0004_topten_updated_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topten",
            name="updated_date",
            field=models.DateField(blank=True, null=True, verbose_name="Updated Date"),
        ),
    ]
