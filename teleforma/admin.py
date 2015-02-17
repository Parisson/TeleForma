# -*- coding: utf-8 -*-
from teleforma.models import *
from teleforma.exam.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class PaymentInline(admin.StackedInline):
    model = Payment

class OptionalFeeInline(admin.StackedInline):
    model = OptionalFee
    extra = 1

class DiscountInline(admin.StackedInline):
    model = Discount
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    model = Student
    exclude = ['options']
    filter_horizontal = ['trainings']
    inlines = [PaymentInline, OptionalFeeInline, DiscountInline]
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_filter = ['user__is_active', 'is_subscribed']
    list_display = ['student_name', 'total_payments', 'total_fees', 'balance']

    def student_name(self, instance):
        return instance.user.last_name + ' ' + instance.user.first_name

    def balance(self, instance):
        return  instance.total_payments - instance.total_fees

class ProfessorProfileInline(admin.StackedInline):
    model = Professor
    filter_horizontal = ['courses']

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor
    filter_horizontal = ['courses']

class ProfileInline(admin.StackedInline):
    model = Profile

class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline]

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
