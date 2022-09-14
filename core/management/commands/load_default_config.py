from core.models import ConfigureSettings
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """Command for loading default configuration"""

    help = "Command for loading default configuration."

    def handle(self, *args, **options):
        obj, created = ConfigureSettings.objects.get_or_create(
            name=settings.LIVE_STOCKS_NSE_500,
            status=False,
        )
