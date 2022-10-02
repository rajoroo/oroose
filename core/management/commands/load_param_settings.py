from core.models import ParameterSettings
from django.core.management.base import BaseCommand
from django.conf import settings
import json


class Command(BaseCommand):
    """Command for loading default configuration"""

    help = "Command for loading default configuration."

    def handle(self, *args, **options):
        json_file = open(settings.LOAD_CONFIG_PATH)
        config_data = json.load(json_file)
        config_sets = config_data["data"]

        configs = {k: v for (k, v) in config_sets.items() if k.startswith('SETTINGS')}

        ParameterSettings.objects.all().delete()
        ParameterSettings.objects.bulk_create([
            ParameterSettings(
                name=key,
                status=value,
            )
            for key, value in configs.items()
        ])
