from django.core.management.base import BaseCommand

from groupme.tasks import morning_digest


class Command(BaseCommand):
    help = 'Runs Daily Digest'

    def handle(self, *args, **options):
        morning_digest()
