from django.core.management.base import BaseCommand



from teleforma.models.core import MediaItemMarker
import json

class Command(BaseCommand):
    help = "Send orders to avis-verifies ftp"

    
    def handle(self, *args, **options):
        data = []

        with open('/srv/src/teleforma/teleforma/export-mediamarkers.json', 'r') as file:
            data = file.read()
        
        data = json.loads(data)
        for row in data:
            if not row['public_id']:
                raise "no public id"
            try:
                marker = MediaItemMarker.objects.get(public_id=row['public_id'], item_id=row['item_id'])
            except MediaItemMarker.DoesNotExist:
                continue
            marker.time = row['time']
            marker.save()
            