# Generated by Django 4.0.7 on 2022-09-15 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_rename_configuration_configuresettings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="configuresettings",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
    ]