from django.conf import settings
from bigbluebutton_api_python import BigBlueButton
from django.core.urlresolvers import reverse

bbb = BigBlueButton(settings.BBB_SERVER, settings.BBB_SECRET)

def register_web_hook():
    if settings.BBB_USE_WEBHOOKS:        
        hook_url =  reverse('webclass_bbb_webhook')
        hook_url = settings.TELEFORMA_MASTER_HOST + hook_url
        bbb.create_hook(hook_url)
    
