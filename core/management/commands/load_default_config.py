from core.models import ConfigureSettings
from django.core.management.base import BaseCommand
from django.conf import settings
import json


class Command(BaseCommand):
    """Command for loading default configuration"""

    help = "Command for loading default configuration."

    def handle(self, *args, **options):
        json_file = open(settings.LOAD_CONFIG_PATH)
        config_data = json.load(json_file)

        configs = config_data["data"]

        ConfigureSettings.objects.all().delete()
        ConfigureSettings.objects.bulk_create([
            ConfigureSettings(
                name=config["name"],
                config_type=config.get("config_type", None),
                boolean_value=config.get("boolean_value", None),
                integer_value=config.get("integer_value", None),
                float_value=config.get("float_value", None),
                string_value=config.get("string_value", None),

            )
            for config in configs
        ])
