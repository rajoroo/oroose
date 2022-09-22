# Generated by Django 4.0.7 on 2022-09-20 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_configuresettings_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="configuresettings",
            name="status",
        ),
        migrations.AddField(
            model_name="configuresettings",
            name="boolean_value",
            field=models.BooleanField(
                blank=True, null=True, verbose_name="Boolean Value"
            ),
        ),
        migrations.AddField(
            model_name="configuresettings",
            name="config_type",
            field=models.CharField(
                choices=[("BOOL", "Boolean"), ("FLOAT", "Float"), ("STRING", "String")],
                default="BOOL",
                max_length=10,
                verbose_name="Configure Type",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="configuresettings",
            name="float_value",
            field=models.FloatField(blank=True, null=True, verbose_name="Float Value"),
        ),
        migrations.AddField(
            model_name="configuresettings",
            name="integer_value",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Integer Value"
            ),
        ),
    ]
