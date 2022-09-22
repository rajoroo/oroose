# Generated by Django 4.1.1 on 2022-09-08 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FiveHundred",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(verbose_name="Date")),
                ("time", models.DateTimeField(verbose_name="Time")),
                ("rank", models.IntegerField(verbose_name="Rank")),
                ("symbol", models.CharField(max_length=200, verbose_name="Symbol")),
                (
                    "identifier",
                    models.CharField(max_length=200, verbose_name="Identifier"),
                ),
                (
                    "company_name",
                    models.CharField(max_length=500, verbose_name="Company Name"),
                ),
                ("isbin", models.CharField(max_length=100, verbose_name="Isbin")),
                ("price", models.FloatField(verbose_name="Price")),
            ],
            options={
                "ordering": ["date", "rank"],
            },
        ),
    ]
