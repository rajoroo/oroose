# Generated by Django 4.0.7 on 2023-03-12 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mysuru", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="topten",
            name="is_valid",
        ),
    ]
