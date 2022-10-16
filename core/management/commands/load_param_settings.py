from core.models import ParameterSettings
from django.core.management.base import BaseCommand

configs = [
    "SETTINGS_FH_LIVE_STOCKS_NSE",
    "SETTINGS_FH_ZERO",
]


class Command(BaseCommand):
    """Command for loading default configuration"""

    help = "Command for loading default configuration."

    def handle(self, *args, **options):
        ParameterSettings.objects.all().delete()
        ParameterSettings.objects.bulk_create([
            ParameterSettings(
                name=item,
                status=False,
            )
            for item in configs
        ])
