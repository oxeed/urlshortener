from django.core.management.base import BaseCommand, CommandError

from shortener.models import ShortURL


class Command(BaseCommand):
    help = 'Refresh shortcodes'

    def handle(self, *args, **options):
        return ShortURL.objects.refresh_shortcodes()