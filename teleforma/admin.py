# -*- coding: utf-8 -*-
import csv
import datetime
from teleforma.admin_filter import MultipleChoiceListFilter
from teleforma.models.chat import ChatMessage

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from .exam.admin import QuotaInline
from .models.appointment import (Appointment, AppointmentJury,
                                 AppointmentPeriod, AppointmentSlot)
from .models.core import (Conference, Course, CourseType, Department, Document,
                          DocumentSimple, DocumentType, LiveStream, Media,
                          MediaTranscoded, Organization, Period, Professor,
                          Room, StreamingServer)
from .models.crfpa import (IEJ, Corrector, Discount, Home, NewsItem,
                           OptionalFee, Parameters, Payback, Payment, Profile,
                           Student, Training)
from .models.messages import GroupedMessage, StudentGroup
from .views.crfpa import CorrectorXLSBook, UserXLSBook



class PeriodListFilter(SimpleListFilter):

    title = _('period')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'period'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """

        return ((period.name, period.name) for period in Period.objects.all())

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(trainings__period__name=self.value())
        else:
            return queryset


class PaymentInline(admin.StackedInline):
    model = Payment


class OptionalFeeInline(admin.StackedInline):
    model = OptionalFee
    extra = 1


class DiscountInline(admin.StackedInline):
    model = Discount
    extra = 1


class PaybackInline(admin.StackedInline):
    model = Payback
    extra = 1


class StudentInline(admin.StackedInline):
    model = Student
    extra = 1

# TODO fix max_length
# class StudentGroupForm(ActionForm):
#     group_name = forms.CharField(_('Group'), required=False)


class StudentGroupAdmin(admin.ModelAdmin):
    model = StudentGroup
    filter_horizontal = ['students']


class BalanceFilter(admin.SimpleListFilter):
    title = _(u'balance')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'balance'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [('ltz', u'négative'),
                ('eqz', u'zéro'),
                ('gtz', u'positive')]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.date()`.
        """
        value = self.value()
        if value == 'ltz':
            return queryset.filter(balance__lt=0)
        elif value == 'eqz':
            return queryset.filter(balance=0)
        elif value == 'gtz':
            return queryset.filter(balance__gt=0)
        else:
            return queryset
class TrainingsFilter(MultipleChoiceListFilter):
    title = 'Formations'
    parameter_name = 'trainings__in'

    def lookups(self, request, model_admin):
        return [(training.id, str(training)) for training in Training.objects.all()]

class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_per_page = 30
    exclude = ['options', 'training']
    filter_horizontal = ['trainings']
    inlines = [PaymentInline, OptionalFeeInline, DiscountInline, PaybackInline]
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_filter = ['user__is_active', 'restricted', 'is_subscribed', 'platform_only', PeriodListFilter,
                   TrainingsFilter, 'iej', 'procedure', 'written_speciality', 'oral_speciality',
                   'oral_1', 'oral_2', 'fascicule', BalanceFilter]
    list_display = ['student_name', 'restricted', 'get_trainings', 'platform_only',
                    'total_payments', 'total_fees', 'balance', 'balance_intermediary']
    readonly_fields = ['balance', 'balance_intermediary']
    actions = ['export_xls', 'write_message', 'add_to_group']
    # action_form = StudentGroupForm

    def get_trainings(self, instance):
        return ' - '.join([str(training) for training in instance.trainings.all()])

    def student_name(self, instance):
        return instance.user.last_name + ' ' + instance.user.first_name

    # def queryset(self, request):
    #     qs = super(StudentAdmin, self).queryset(request)
    #     qs = qs.annotate(models.Count('warehouse__amount'))
    #     return qs

    def export_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response

    def export_xls(self, request, queryset):
        book = UserXLSBook(students=queryset)
        book.write()
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=users.xls'
        book.book.save(response)
        return response

    export_xls.short_description = "Export vers XLS"

    def add_to_group(self, request, queryset):
        group_name = request.POST['group_name']
        group, c = StudentGroup.objects.get_or_create(name=group_name)
        for student in queryset:
            group.students.add(student)
        # self.message_user(request, ("Successfully added to group : %s") % (group_name,), messages.SUCCESS)
    add_to_group.short_description = "Ajouter au groupe"


class CorrectorAdmin(admin.ModelAdmin):
    model = Corrector
    list_filter = ['user__is_active', 'period']
    list_display = ['__str__', 'period', 'pay_status',
                    'date_registered']
    actions = ['export_xls']
    search_fields = ['user__username', 'user__first_name',
                     'user__last_name', 'user__email']

    def export_xls(self, request, queryset):
        book = CorrectorXLSBook(correctors=queryset)
        book.write()
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=correcteurs.xls'
        book.book.save(response)
        return response

    export_xls.short_description = "Export vers XLS"


class ProfessorProfileInline(admin.StackedInline):
    model = Professor
    filter_horizontal = ['courses']


class ProfessorAdmin(admin.ModelAdmin):
    model = Professor
    filter_horizontal = ['courses']


class ProfileInline(admin.StackedInline):
    model = Profile


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline, StudentInline, QuotaInline]
    search_fields = ['username', 'email']


class TrainingAdmin(admin.ModelAdmin):
    model = Training
    filter_horizontal = ['synthesis_note', 'obligation', 'procedure', 'oral_speciality',
                         'written_speciality', 'oral_1', 'oral_2', 'magistral']
    exclude = ['options']


class CourseAdmin(admin.ModelAdmin):
    model = Course
    ordering = ['number']


class DocumentAdmin(admin.ModelAdmin):
    list_per_page = 30
    exclude = ['readers']
    filter_horizontal = ['course_type']
    list_filter = ('course', 'periods', 'date_added', 'type')
    search_fields = ['course__code', 'course__title', 'type__name']


class ConferenceDateBeginFilter(admin.SimpleListFilter):
    title = _(u'date de début')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'date_begin'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        conferences = Conference.objects.all()
        dates = [c.date_begin.date() for c in conferences if c.date_begin]
        dates = set(dates)
        res = [(d.strftime('%Y%m%d'), d.strftime('%d/%m/%Y')) for d in dates]
        return sorted(res)[::-1]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.date()`.
        """
        value = self.value()
        if value:
            date = datetime.date(int(value[:4]), int(
                value[4:6]), int(value[6:]))
            rng = (datetime.datetime.combine(date, datetime.time.min),
                   datetime.datetime.combine(date, datetime.time.max))
            return queryset.filter(conference__date_begin__range=rng)
        else:
            return queryset


class MediaTranscodedInline(admin.TabularInline):
    model = MediaTranscoded


def duplicate_object(obj):
    """
    Duplicate a model instance, making copies of all foreign keys pointing to it.
    There are 3 steps that need to occur in order:

        1.  Enumerate the related child objects and m2m relations, saving in lists/dicts
        2.  Copy the parent object per django docs (doesn't copy relations)
        3a. Copy the child objects, relating to the copied parent object
        3b. Re-create the m2m relations on the copied parent object

    """
    related_objects_to_copy = []
    relations_to_set = {}
    # Iterate through all the fields in the parent object looking for related fields
    for field in obj._meta.get_fields():
        if field.one_to_many:
            # One to many fields are backward relationships where many child
            # objects are related to the parent. Enumerate them and save a list
            # so we can copy them after duplicating our parent object.
            print(f'Found a one-to-many field: {field.name}')

            # 'field' is a ManyToOneRel which is not iterable, we need to get
            # the object attribute itobj.
            related_object_manager = getattr(obj, field.name)
            related_objects = list(related_object_manager.all())
            if related_objects:
                print(f' - {len(related_objects)} related objects to copy')
                related_objects_to_copy += related_objects

        elif field.many_to_one:
            # In testing, these relationships are preserved when the parent
            # object is copied, so they don't need to be copied separately.
            print(f'Found a many-to-one field: {field.name}')

        elif field.many_to_many:
            # Many to many fields are relationships where many parent objects
            # can be related to many child objects. Because of this the child
            # objects don't need to be copied when we copy the parent, we just
            # need to re-create the relationship to them on the copied parent.
            print(f'Found a many-to-many field: {field.name}')
            related_object_manager = getattr(obj, field.name)
            relations = list(related_object_manager.all())
            if relations:
                print(f' - {len(relations)} relations to set')
                relations_to_set[field.name] = relations

    # Duplicate the parent object
    obj.pk = None
    obj.save()
    print(f'Copied parent object ({str(obj)})')

    # Copy the one-to-many child objects and relate them to the copied parent
    for related_object in related_objects_to_copy:
        # Iterate through the fields in the related object to find the one that
        # relates to the parent model.
        for related_object_field in related_object._meta.fields:
            if related_object_field.related_model == obj.__class__:
                # If the related_model on this field matches the parent
                # object's class, perform the copy of the child object and set
                # this field to the parent object, creating the new
                # child -> parent relationship.
                related_object.pk = None
                setattr(related_object, related_object_field.name, obj)
                related_object.save()

                text = str(related_object)
                text = (text[:40] + '..') if len(text) > 40 else text
                print(f'|- Copied child object ({text})')

    # Set the many-to-many relations on the copied parent
    for field_name, relations in relations_to_set.items():
        # Get the field by name and set the relations, creating the new
        # relationships.
        field = getattr(obj, field_name)
        field.set(relations)
        text_relations = []
        for relation in relations:
            text_relations.append(str(relation))
        print(f'|- Set {len(relations)} many-to-many relations on {field_name} {text_relations}')

    return obj


@admin.action(description='Duplicate selected objects')
def duplicate(modeladmin, request, queryset):
    for obj in queryset:
        duplicate_object(obj)


class MediaAdmin(admin.ModelAdmin):
    list_per_page = 30
    exclude = ['readers']
    search_fields = ['id', 'title', 'course__title', 'course__code']
    list_filter = (ConferenceDateBeginFilter, )
    inlines = [MediaTranscodedInline]
    actions = [duplicate,]


class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers']
    list_per_page = 30
    list_filter = ('course', 'period', 'date_begin', 'session')
    search_fields = ['public_id', 'id',
                     'course__code', 'course__title', 'session']


class HomeAdmin(admin.ModelAdmin):
    list_filter = ('enabled',)
    search_fields = ['periods__name', 'title', 'text']
    list_display = ('title', 'enabled', 'modified_at')
    readonly_fields = ('modified_at',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(HomeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['video'].queryset = Media.objects.filter(type='webm')
        return form


class ParametersAdmin(admin.ModelAdmin):
    pass


class NewsItemAdmin(admin.ModelAdmin):
    list_filter = ('deleted', 'course', 'creator')
    list_display = ('title', 'course', 'creator', 'deleted')
    search_fields = ['title', 'text']


class AppointmentSlotInline(admin.TabularInline):
    model = AppointmentSlot
    list_per_page = 30


class AppointmentJuryInline(admin.StackedInline):
    model = AppointmentJury


# class AppointmentDayInline(admin.TabularInline):
#     readonly_fields = ('get_nb_slots', 'get_nb_jury', 'changeform_link', )
#     model = AppointmentDay


class AppointmentPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'periods_names', 'start',
                    'end', 'enable_appointment')

    # inlines = [ AppointmentDayInline ]

    def periods_names(self, instance):
        return ','.join([period.name for period in instance.periods.all()])
    periods_names.short_description = "Périodes"

# class AppointmentDayAdmin(admin.ModelAdmin):
#     list_filter = ('appointment_period',)
#     list_display = ('date', 'appointment_period', 'get_nb_slots', 'get_nb_jury')
#
#     inlines = [ AppointmentSlotInline, AppointmentJuryInline ]


class AppointmentSlotAdmin(admin.ModelAdmin):
    list_filter = ('date', 'appointment_period')
    list_display = ('date', 'appointment_period',
                    'mode', 'start', 'nb', 'get_nb_jury')
    inlines = [AppointmentJuryInline]


class AppointmentJuryAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_filter = ('slot',)
    list_display = ('name', 'slot')


class AppointmentAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('real_date', 'student', 'jury')
    list_filter = ('slot__date', 'slot__appointment_period', 'slot__mode')
    search_fields = ('student__username',)
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=rendezvous.csv'
        writer = csv.writer(response)

        writer.writerow(['date', 'creneau', 'nom', 'prenom',
                        'email', 'iej', 'jury', 'mode'])

        def csv_encode(item):
            return item

        for app in queryset:
            user = app.student
            student = user.student.all()[0]

            row = [app.day.strftime('%d/%m/%Y'), app.start, user.last_name,
                   user.first_name, user.email, student.iej, app.jury.name, app.slot.mode]
            row = [csv_encode(col) for col in row]

            writer.writerow(row)

        return response
    export_csv.short_description = "Exporter en CSV"

class GroupedMessageAdmin(admin.ModelAdmin):
    list_per_page = 30    

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'room_name')
    ordering = ['-created']
    raw_id_fields = ['user',]


admin.site.unregister(User)
admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Period)
admin.site.register(Course, CourseAdmin)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(IEJ)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentSimple)
admin.site.register(DocumentType)
admin.site.register(Media, MediaAdmin)
admin.site.register(Room)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(CourseType)
admin.site.register(StreamingServer)
admin.site.register(LiveStream)
admin.site.register(Student, StudentAdmin)
admin.site.register(Corrector, CorrectorAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(StudentGroup, StudentGroupAdmin)
admin.site.register(GroupedMessage, GroupedMessageAdmin)
admin.site.register(Home, HomeAdmin)
admin.site.register(Parameters, ParametersAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(AppointmentPeriod, AppointmentPeriodAdmin)
# admin.site.register(AppointmentDay, AppointmentDayAdmin)
admin.site.register(AppointmentSlot, AppointmentSlotAdmin)
admin.site.register(AppointmentJury, AppointmentJuryAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
