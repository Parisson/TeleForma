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
                
