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


class ConfigType(models.TextChoices):
    BOOL = "BOOL", "Boolean"
    CHAR = "CHAR", "String"
    TEXT = "TEXT", "Text"
    FLOAT = "FLOAT", "Float"
    INT = "INT", "Integer"
    DATE = "DATE", "Date"


class ParameterConfig(models.Model):
    date = models.DateField(verbose_name="Date")
    name = models.CharField(max_length=100, verbose_name="Name")
    nick_name = models.CharField(max_length=100, verbose_name="Nick Name")
    tag = models.CharField(max_length=20, verbose_name="Tag")
    config_type = models.CharField(
        max_length=10,
        choices=ConfigType.choices,
        verbose_name="Type",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    comment = models.TextField(blank=True, null=True, verbose_name="Comment")
    content_bool = models.BooleanField(verbose_name="Boolean", blank=True, null=True)
    content_char = models.CharField(max_length=100, verbose_name="Char", blank=True, null=True)
    content_text = models.TextField(verbose_name="Text", blank=True, null=True)
    content_float = models.FloatField(verbose_name="Float", blank=True, null=True)
    content_int = models.IntegerField(verbose_name="Integer", blank=True, null=True)
    content_date = models.DateField(verbose_name="Date", blank=True, null=True)

    objects = models.Manager()

    @property
    def content(self):
        attr = f"content_{self.config_type.lower()}"
        return getattr(self, attr)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["nick_name"], name="%(app_label)s_%(class)s_unique_parameter_configs"
            )
        ]
