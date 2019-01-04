# -*- coding: utf-8 -*-
from telemeta.util.unicode import UnicodeWriter
from teleforma.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from longerusername.forms import UserCreationForm, UserChangeForm
from django.contrib.contenttypes.generic import GenericInlineModelAdmin
from django.http import HttpResponse

class ProfileInline(admin.StackedInline):
    model = Profile

class CRFPAStudentProfileInline(admin.StackedInline):
    model = Student
    filter_horizontal = ['period']
    exclude = ['options']

class AEStudentProfileInline(admin.StackedInline):
    model = AEStudent
    filter_horizontal = ['period', 'courses']

class AuditorProfileInline(admin.StackedInline):
    model = Auditor
    filter_vertical = ['seminars', 'conferences']

    class Media:
        css = { 'all': ('admin/extra.css',) }

class StudentAdmin(admin.ModelAdmin):
    model = Student
    exclude = ['options']

class ProfessorProfileInline(admin.StackedInline):
    model = Professor
    filter_horizontal = ['courses']

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor
    filter_horizontal = ['courses']

class UserProfileAdmin(UserAdmin):
    inlines = [ProfessorProfileInline, AuditorProfileInline]
    add_form = UserCreationForm
    form = UserChangeForm

class TrainingAdmin(admin.ModelAdmin):
    model = Training
    filter_horizontal = ['synthesis_note', 'obligation', 'procedure', 'oral_speciality',
                         'written_speciality', 'oral_1', 'oral_2','magistral']
    exclude = ['options']

class CourseAdmin(admin.ModelAdmin):
    model = Course
    ordering = ['number']
    filter_horizontal = ['types']

class CourseDomainAdmin(admin.ModelAdmin):
    filter_horizontal = ['courses']

class DocumentAdmin(admin.ModelAdmin):
    exclude = ['readers']
    filter_horizontal = ['course_type']
    search_fields = ['title', 'course__title', 'course__code']
    list_filter = ('period', 'date_added')

class MediaAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['id', 'title', 'course__title', 'course__code']
    list_filter = ('period', 'date_added')

class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['public_id', 'id']
    filter_vertical = ['docs_description',
                       'suggested_seminars', 'suggested_conferences']

class SeminarQuestionInline(admin.StackedInline):
    model = Question

class SeminarAdmin(admin.ModelAdmin):
    inlines = [SeminarQuestionInline,]
    filter_horizontal = ['professor',]
    filter_vertical = ['docs_description', 'docs_1',
                       'docs_2', 'docs_correct', 'medias',
                       'suggested_seminars', 'suggested_conferences']
    ordering = ['course', 'rank']
    search_fields = ['course__title', 'title', 'sub_title']
    list_filter = ('period', 'publish_date', 'expiry_date')

    class Media:
        css = { 'all': ('admin/extra.css',) }

class MediaItemMarkerAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']


class TestimonialAdmin(admin.ModelAdmin):
    search_fields = ['seminar__course__title', 'seminar__sub_title',
                    'user__username', 'user__last_name']


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__last_name']


class SeminarRevisionAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'seminar__title']
    date_hierarchy = 'date_modified'

    actions = ['export_seminar_revisions']

    def export_seminar_revisions(self, request, queryset):

        def pretty_duration(delta):
            seconds = delta.total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            duration = "%d heures %d minutes %d secondes" % (hours, minutes, seconds)
            return duration

        response = HttpResponse(content_type='text/csv')
        filename = "releve-revision"
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename

        data = {}
        for rev in queryset.order_by('-date'):
            seminar_id = rev.seminar.id
            if seminar_id not in data:
                data[seminar_id] = {'title': rev.seminar.pretty_title.encode('utf-8'), 'users': {}}

            user = rev.user.email
            if user not in data[seminar_id]['users']:
                data[seminar_id]['users'][user] = []

            if rev.date_modified:
                data[seminar_id]['users'][user].append({'start': rev.date, 'end': rev.date_modified})

        writer = UnicodeWriter(response, delimiter=";")
        writer.writerow(["seminaire", "email", "duree total", "date debut", "date fin", "duree"])
        for seminar in data.keys():
            title = data[seminar]['title']
            users = data[seminar]['users']
            for user in users.keys():
                l = [title, user]
                revs = users[user]
                duration = datetime.timedelta()
                for rev in revs:
                    diff = rev['end'] - rev['start'] if rev['end'] else datetime.timedelta()
                    if diff.total_seconds() < 0:
                        continue
                    l.append(str(rev['start']))
                    l.append(str(rev['end']))
                    l.append(pretty_duration(rev['end'] - rev['start']) if rev['end'] else 0)
                    duration += rev['end'] - rev['start'] if rev['end'] else datetime.timedelta()
                l.insert(2, pretty_duration(duration))
                writer.writerow(l)
        return response

    export_seminar_revisions.short_description = "Exporter le relevé des temps de connexion"


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(SeminarRevision, SeminarRevisionAdmin)

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Period)
# admin.site.register(Training, TrainingAdmin)

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType)
admin.site.register(CourseDomain, CourseDomainAdmin)
admin.site.register(Conference, ConferenceAdmin)
# admin.site.register(IEJ)
admin.site.register(Professor, ProfessorAdmin)

admin.site.register(Seminar, SeminarAdmin)
admin.site.register(Question)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(TestimonialTemplate)
admin.site.register(SeminarType)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuizValidation)

admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentType)
admin.site.register(Media, MediaAdmin)
admin.site.register(Room)

admin.site.register(StreamingServer)
admin.site.register(LiveStream)

# TELEMETA
admin.site.register(MediaItemMarker, MediaItemMarkerAdmin)
