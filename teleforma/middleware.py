from telemeta.models.system import *
from teleforma.models import *


class OnlyOneUser(object):

    def process_request(self, request):
        if not request.user.is_anonymous():
            profile = UserProfile.objects.get(user=request.user)
            cur_session_key = profile.last_session_key
            if cur_session_key and cur_session_key != request.session.session_key:
                sessions = Session.objects.filter(session_key=cur_session_key)
                if sessions:
                    for session in sessions:
                        Session.objects.get(session_key=cur_session_key).delete()
            #the following can be optimized(do not save each time if value not changed)
            profile.session_key = request.session.session_key
            profile.save()


class ItemExportSecurity(object):

    def process_view(self, request, ItemView.item_export, *args, **kwargs):
        id = args[0]
        ext = args[1]
        item = MediaItem.objects.get(public_id=id)
        student = request.user.student.all()
        if student:
            courses = request.user.student.get().training.courses.all()
            media = item.media.all()
            if media:
                media_courses = media.course.all()
                for course in media_courses:
                    if not course in courses:
                        return 404
                    else:
                        return None
            else:
                return None
        else:
            return None
                
import re
 
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers
 
from django import http
 
try:
    import settings 
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
    XS_SHARING_ALLOWED_HEADERS = settings.XS_SHARING_ALLOWED_HEADERS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
    XS_SHARING_ALLOWED_HEADERS = ['Origin', 'Content-Type', 'Accept']
 
 
class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         
 
        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):
 
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS ) 
            
            return response
 
        return None
 
    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
 
        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS ) 
 
        return response
