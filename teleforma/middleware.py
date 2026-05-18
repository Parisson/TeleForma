from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models.expressions import F
from django import http

try:
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
    XS_SHARING_ALLOWED_HEADERS = settings.XS_SHARING_ALLOWED_HEADERS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']
    XS_SHARING_ALLOWED_HEADERS = ['Origin', 'Content-Type', 'Accept']


class XsSharing:
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.


        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join(
                XS_SHARING_ALLOWED_METHODS)
            response['Access-Control-Allow-Headers'] = ",".join(
                XS_SHARING_ALLOWED_HEADERS)

        return self.get_response(request)

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return self.get_response(request)

        response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = ",".join(
            XS_SHARING_ALLOWED_METHODS)
        response['Access-Control-Allow-Headers'] = ",".join(
            XS_SHARING_ALLOWED_HEADERS)

        return self.get_response(request)


class LastUserActivityMiddleware:
    KEY = "last-activity"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            last_activity = request.session.get(self.KEY)
            too_old_time = now - timedelta(seconds=settings.LAST_ACTIVITY_INTERVAL_SECS)

            # Update database only if the session timestamp is old enough
            if not last_activity or last_activity < too_old_time:
                # Update your custom UserActivity or UserProfile model
                request.user.last_login = now
                request.user.save()

            # Update the session timestamp
            request.session[self.KEY] = now.isoformat()

        return self.get_response(request)