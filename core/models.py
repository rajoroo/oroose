from django.db import models


class DataLog(models.Model):
    date = models.DateField(verbose_name="Date")
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time", null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name="Name")

    objects = models.Manager()
