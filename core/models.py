from django.db import models


class DataLog(models.Model):
    date = models.DateField(verbose_name="Date")
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time", null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name="Name")

    objects = models.Manager()

    class Meta:
        ordering = ["-start_time"]


class ParameterSettings(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    status = models.BooleanField(default=False, verbose_name="Status")

    objects = models.Manager()

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "status"], name="%(app_label)s_%(class)s_unique_parameter_settings"
            )
        ]


class ParameterConfig(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    nick_name = models.CharField(max_length=200, verbose_name="Nick Name")
    tag = models.CharField(max_length=200, verbose_name="Tag")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    comment = models.TextField(blank=True, null=True, verbose_name="Comment")
    content = models.CharField(max_length=200, verbose_name="Content")

    objects = models.Manager()

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["nick_name"], name="%(app_label)s_%(class)s_unique_parameter_configs"
            )
        ]
