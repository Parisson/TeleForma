from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = "Change Site domain to another"
    
    def handle(self, *args, **options):
        to_domain = args[1]
        from_domain = args[0]

        site = Site.objects.get(domain=from_domain)
        site.domain = to_domain
        site.save()
