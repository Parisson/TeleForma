# -*- coding: utf-8 -*-
from teleforma.utils.unicode import UnicodeWriter
from teleforma.models import *
from teleforma.templatetags.teleforma_tags import fancy_duration_shop_like, fancy_seconds
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# from longerusername.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
import time
from datetime import date

class CRFPAStudentProfileInline(admin.StackedInline):
    model = Student
    filter_horizontal = ['period']
    exclude = ['options']

class AEStudentProfileInline(admin.StackedInline):
    model = AEStudent
    filter_horizontal = ['period', 'courses']

class AuditorProfileInline(admin.StackedInline):
    model = Auditor
    # filter_vertical = ['seminars', 'conferences']

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
    # add_form = UserCreationForm
    # form = UserChangeForm
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']

    actions = ['export_user_profiles']

    def export_user_profiles(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        filename = "export-utilisateurs-%s" % time.strftime('%Y-%m-%d')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename
        
        users = []
        for user in queryset.order_by('email'):
            auditor = list(user.auditor.all())
            auditor = auditor and auditor[0] or None
            if user.is_superuser:
                account_type = "admin"
            elif auditor:
                account_type = "auditeur"
            elif user.professor:
                account_type = "professeur"
            else:
                account_type = "autre"
            conferences = []
            seminars = []
            if auditor:
                for conf in auditor.conferences.all().order_by('pk'):
                    conferences.append('%s (%s)' % (conf, conf.pk))
                for sem in auditor.seminars.all().order_by('pk'):
                    seminars.append('%s (%s)' % (sem, sem.pk))
            l = [ user.email,
                  user.first_name,
                  user.last_name,
                  auditor and auditor.address or '',
                  auditor and auditor.postal_code or '',
                  auditor and auditor.city or '',
                  auditor and auditor.country,
                  account_type,
                  user.date_joined.strftime('%d/%m/%Y'),
                  user.last_login.strftime('%d/%m/%Y'),
            ]
            users.append({ 'data': l,
                           'seminars': seminars,
                           'conferences': conferences })

        maxconf = max([ len(u['conferences']) for u in users ] + [ 1 ])
        maxsem = max([ len(u['seminars']) for u in users ] + [ 1 ])
        
        writer = UnicodeWriter(response, delimiter=";")
        titlerow = ["email",
                         "prénom",
                         "nom",
                         "adresse",
                         "code postal",
                         "ville",
                         "pays",
                         "type de compte",
                         "date de création",
                         "date de dernière connexion", ]
        for i in range(maxconf):
            titlerow.append('conférence %d' % (i+1))
        for i in range(maxsem):
            titlerow.append('séminaire %d' % (i+1))
        writer.writerow(titlerow)
        for user in users:
            l = user['data']
            nbconf = len(user['conferences'])
            nbsem = len(user['seminars'])
            for i in range(maxconf):                
                l.append(user['conferences'][i] if i < nbconf else '')
            for i in range(maxsem):                
                l.append(user['seminars'][i] if i < nbsem else '')
            writer.writerow(l)
        return response

    export_user_profiles.short_description = "Exporter les utilisateurs"
    
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

class MediaTranscodedInline(admin.TabularInline):
    model = MediaTranscoded

class MediaAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    exclude = ['readers']
    search_fields = ['id', 'title', 'course__title', 'course__code', 'item__title']
    inlines = [MediaTranscodedInline]

class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers', 'keywords']
    search_fields = ['public_id', 'id', 'title']
    # filter_vertical = ['docs_description',
    #                    'suggested_seminars', 'suggested_conferences']
    actions = ['export_conference']

    def render_change_form(self, request, context, *args, **kwargs):
        """
        Filter queryset to improve performance
        """
        instance = context.get('original')
        current_year = date.today().year
        years = (str(current_year), str(current_year - 1))
        current_values = []
        if instance:
            current_values = [doc.id for doc in instance.docs_description.all()]
        context['adminform'].form.fields['docs_description'].queryset = Document.objects.filter(
            Q(period__name__in=years) | 
            Q(id__in=current_values)
        )
        # if instance:
        #     current_values = [doc.id for doc in instance.suggested_seminars.all()]
        # context['adminform'].form.fields['suggested_seminars'].queryset = Seminar.objects.filter(
        #     Q(private=2) | 
        #     Q(id__in=current_values)
        # )
        # if instance:
        #     current_values = [doc.id for doc in instance.suggested_conferences.all()]
        # context['adminform'].form.fields['suggested_conferences'].queryset = Conference.objects.filter(
        #     Q(status=2) | 
        #     Q(id__in=current_values)
        # )
        return super(ConferenceAdmin, self).render_change_form(request, context, *args, **kwargs)

    def export_conference(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        filename = "conferences"
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename

        data = {}
        writer = UnicodeWriter(response, delimiter=";")
        writer.writerow(("id", "nom", "prix", "code produit"))

        for conference in queryset.order_by('-publish_date'):
            title = conference.pretty_title
            
            if conference.webclass:
                title = "Webconférence - " + title
            if conference.duration:
                title += " - Durée : %s" % (fancy_duration_shop_like(conference.duration))
            if conference.webclass:
                title += " (%s live + %s de validation des acquis)" % (fancy_seconds(conference.webclass_duration), fancy_seconds(conference.webclass_hours_complementary.as_seconds()))
            row = (conference.id, title, conference.price, conference.product_code)
            writer.writerow(row)
        return response

    export_conference.short_description = "Exporter les conferences"


class SeminarQuestionInline(admin.StackedInline):
    model = Question

class SeminarAdmin(admin.ModelAdmin):
    exclude = ['keywords']
    inlines = [SeminarQuestionInline,]
    filter_horizontal = ['professor',]
    # filter_vertical = ['docs_description', 'docs_1',
    #                    'docs_2', 'docs_correct', 'medias',
    #                    'suggested_seminars', 'suggested_conferences']
    ordering = ['course', 'rank']
    search_fields = ['course__title', 'title', 'sub_title']
    list_filter = ('period', 'publish_date', 'expiry_date')
    actions = ['clone_seminars', 'export_seminar']
    raw_id_fields = [ 'media_preview',
                      'quiz', 'conference']

    def render_change_form(self, request, context, *args, **kwargs):
        """
        Filter queryset to improve performance
        """
        instance = context.get('original')
        current_year = date.today().year
        years = (str(current_year), str(current_year - 1))
        # Documents
        for fieldname in ('docs_description', 'docs_1', 'docs_2', 'docs_correct'):
            current_values = []
            if instance:
                current_values = getattr(instance, fieldname).all()
            context['adminform'].form.fields[fieldname].queryset = Document.objects.filter(
                Q(period__name__in=years) | 
                Q(id__in=[doc.id for doc in current_values])
            )

        # Medias
        current_values = []
        if instance:
            current_values = instance.medias.all()
        context['adminform'].form.fields['medias'].queryset = Media.objects.filter(
            Q(date_modified__gte=datetime.date(current_year - 1, 1, 1)) | 
            Q(id__in=[media.id for media in current_values])
        )
        preview_id = None
        if instance and instance.media_preview:
            preview_id = instance.media_preview.id
        context['adminform'].form.fields['media_preview'].queryset = Media.objects.filter(
            Q(date_modified__gte=datetime.date(current_year - 1, 1, 1)) | 
            Q(id=preview_id)
        )
        
        return super(SeminarAdmin, self).render_change_form(request, context, *args, **kwargs)

    def clone_seminars(self, request, queryset):
        log = ""
        for seminar in queryset:
            log += seminar.clone_to_next_year()
            log += "\n"
        return HttpResponse(log)
            
    clone_seminars.short_description = "Dupliquer les séminaires"


    def export_seminar(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        filename = "seminaires"
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % filename

        data = {}
        writer = UnicodeWriter(response, delimiter=";")
        writer.writerow(("id", "nom", "prix", "code produit"))

        for seminar in queryset.order_by('-publish_date'):
            row = (seminar.id, seminar.pretty_title_with_duration, seminar.price, seminar.product_code)
            writer.writerow(row)
        return response

    export_seminar.short_description = "Exporter les séminaires"

    class Media:
        css = { 'all': ('admin/extra.css',) }

class MediaItemMarkerAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']


class TestimonialAdmin(admin.ModelAdmin):
    search_fields = ['seminar__course__title', 'seminar__sub_title',
                    'user__username', 'user__last_name']


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__last_name']
    list_filter = ['status', 'treated', 'validated', 'date_submitted', 'date_validated', 'question__seminar']
    list_display = ['question', 'user', 'status', 'treated', 'validated', 'date_submitted', 'date_validated']



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
        for seminar in list(data.keys()):
            title = data[seminar]['title']
            users = data[seminar]['users']
            for user in list(users.keys()):
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
