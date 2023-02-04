from django.contrib import admin
from core.models import ParameterConfig


@admin.register(ParameterConfig)
class ParameterConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "nick_name",
        "tag",
        "content"
    )
