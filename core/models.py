from django.db import models


class ConfigureSettings(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    status = models.BooleanField(default=False, verbose_name="Status")

    objects = models.Manager()
