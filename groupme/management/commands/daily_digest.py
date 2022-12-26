from django.core.management.base import BaseCommand

from groupme.tasks import morning_digest


class Command(BaseCommand):
    help = 'Runs Daily Digest'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        morning_digest()
