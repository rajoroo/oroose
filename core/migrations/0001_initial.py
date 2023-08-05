# Generated by Django 4.2.1 on 2023-08-06 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ParameterConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="Date")),
                ("sequence", models.IntegerField(verbose_name="Sequence")),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                ("nick_name", models.CharField(max_length=100, verbose_name="Nick Name")),
                ("tag", models.CharField(max_length=20, verbose_name="Tag")),
                (
                    "config_type",
                    models.CharField(
                        choices=[
                            ("BOOL", "Boolean"),
                            ("CHAR", "String"),
                            ("TEXT", "Text"),
                            ("FLOAT", "Float"),
                            ("INT", "Integer"),
                            ("DATE", "Date"),
                        ],
                        max_length=10,
                        verbose_name="Type",
                    ),
                ),
                ("description", models.TextField(blank=True, null=True, verbose_name="Description")),
                ("comment", models.TextField(blank=True, null=True, verbose_name="Comment")),
                ("content_bool", models.BooleanField(blank=True, null=True, verbose_name="Boolean")),
                ("content_char", models.CharField(blank=True, max_length=100, null=True, verbose_name="Char")),
                ("content_text", models.TextField(blank=True, null=True, verbose_name="Text")),
                ("content_float", models.FloatField(blank=True, null=True, verbose_name="Float")),
                ("content_int", models.IntegerField(blank=True, null=True, verbose_name="Integer")),
                ("content_date", models.DateField(blank=True, null=True, verbose_name="Date")),
            ],
            options={
                "ordering": ["tag", "sequence"],
            },
        ),
        migrations.AddConstraint(
            model_name="parameterconfig",
            constraint=models.UniqueConstraint(
                fields=("nick_name",), name="core_parameterconfig_unique_parameter_configs"
            ),
        ),
    ]
