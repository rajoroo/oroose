# Generated by Django 4.0.7 on 2022-10-17 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datalog',
            options={'ordering': ['-start_time']},
        ),
    ]