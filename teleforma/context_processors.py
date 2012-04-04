from django.contrib.sites.models import Site

def main(request):
    return {'site': Site.objects.get_current()}



