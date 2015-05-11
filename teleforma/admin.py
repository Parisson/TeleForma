# -*- coding: utf-8 -*-
from teleforma.models import *
from teleforma.views import *
from teleforma.exam.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.core import serializers


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
        return ( (period.name, period.name) for period in Period.objects.all() )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return queryset.filter(trainings__period__name=self.value())


class PaymentInline(admin.StackedInline):
    model = Payment

class OptionalFeeInline(admin.StackedInline):
    model = OptionalFee
    extra = 1

class DiscountInline(admin.StackedInline):
    model = Discount
    extra = 1

class StudentInline(admin.StackedInline):
    model = Student
    extra = 1


class StudentAdmin(admin.ModelAdmin):

    model = Student
    exclude = ['options']
    filter_horizontal = ['trainings']
    inlines = [PaymentInline, OptionalFeeInline, DiscountInline]
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_filter = [PeriodListFilter, 'user__is_active', 'is_subscribed', 'trainings', 'iej',
                    'procedure', 'written_speciality', 'oral_speciality',
                    'oral_1', 'oral_2']
    list_display = ['student_name', 'total_payments', 'total_fees', 'balance']
    actions = ['export_xls']

    def student_name(self, instance):
        return instance.user.last_name + ' ' + instance.user.first_name

    def balance(self, instance):
        return  round(instance.total_payments - instance.total_fees, 2)

    # def queryset(self, request):
    #     qs = super(StudentAdmin, self).queryset(request)
    #     qs = qs.annotate(models.Count('warehouse__amount'))
    #     return qs

    def export_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response

    def export_xls(self, request, queryset):
        users = [student.user for student in queryset]
        book = UserXLSBook(users)
        book.write()
        response = HttpResponse(mimetype="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=users.xls'
        book.book.save(response)
        return response

    export_xls.short_description = "Export to XLS"



class ProfessorProfileInline(admin.StackedInline):
    model = Professor
    filter_horizontal = ['courses']

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor
    filter_horizontal = ['courses']

class ProfileInline(admin.StackedInline):
    model = Profile

class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline, StudentInline]

class TrainingAdmin(admin.ModelAdmin):
    model = Training
    filter_horizontal = ['synthesis_note', 'obligation', 'procedure', 'oral_speciality',
                         'written_speciality', 'oral_1', 'oral_2','magistral']
    exclude = ['options']

class CourseAdmin(admin.ModelAdmin):
    model = Course
    ordering = ['number']

class QuotaAdmin(admin.ModelAdmin):
    model = Quota

class DocumentAdmin(admin.ModelAdmin):
    exclude = ['readers']
    filter_horizontal = ['course_type']
    search_fields = ['course__code', 'course__title']
    list_filter = ('period', 'date_added')

class MediaAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['id', 'title', 'course__title', 'course__code']

class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['public_id', 'id', 'course__code', 'course__title']


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
admin.site.register(Professor, ProfessorAdmin)
