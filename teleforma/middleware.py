from telemeta.models.system import *
from teleforma.models import *


class OnlyOneUserMiddleware(object):

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


class ExportSecurity(object):

    def process_view(self, item_export):
        pass
        
