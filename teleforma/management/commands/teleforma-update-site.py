from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = "Change Site domain to another"

    def add_arguments(self, parser):
        parser.add_argument(
            '--from',
            action='store_true',
            help='from domain',
        )
        parser.add_argument(
            '--to',
            action='store_true',
            help='to domain',
        )


    def handle(self, *args, **options):
        from_domain = options['from']
        to_domain = options['to']

        site = Site.objects.get(domain=from_domain)
        site.domain = to_domain
        site.save()
