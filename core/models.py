from django.db import models


class ConfigureType(models.TextChoices):
    BOOLEAN = "BOOL", "Boolean"
    INTEGER = "INTEGER", "Integer"
    FLOAT = "FLOAT", "Float"
    STRING = "STRING", "String"


class ConfigureSettings(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Name"
    )
    config_type = models.CharField(
        max_length=10,
        choices=ConfigureType.choices,
        verbose_name="Configure Type",
    )
    boolean_value = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Boolean Value"
    )
    integer_value = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Integer Value"
    )
    float_value = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Float Value"
    )
    string_value = models.TextField(
        blank=True,
        null=True,
        verbose_name="Text Value"
    )

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='%(app_label)s_%(class)s_unique')
        ]

    def render_status(self):
        return self.boolean_value
