import requests
from django import template
from django.conf import settings
import teleforma

register = template.Library()

@register.inclusion_tag('teleforma/webpack.html')
def webpack(bundle):
    """
    """
    url = '/static/teleforma/dist/%s' % bundle
    is_css = False
    if bundle.split('.')[1] == 'css':
        is_css = True
        # test if js from same bundle is available. If true, then the css code is in the js file
        bundle = bundle.split('.')[0] + '.js'
    if settings.USE_WEBPACK_DEV_SERVER:
        try:
            WEBPACK_APP_URL = '{}{}'.format(settings.WEBPACK_DEV_SERVER_URL, bundle)
            request = requests.get(WEBPACK_APP_URL)
            if request.status_code == 200:
                # host.docker.internal is only available in the context of the container, not in the browser
                url = WEBPACK_APP_URL.replace('host.docker.internal', 'localhost')
                if is_css:
                    url = None
        except requests.ConnectionError:
            pass

    if url:
        url += '?v=' + teleforma.__version__

    return {
        'is_css': is_css,
        'url': url
    }
