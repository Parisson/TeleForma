# -*- coding: utf-8 -*-
from teleforma.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CRFPAStudentProfileInline(admin.StackedInline):
    model = Student
    exclude = ['options']
    filter_horizontal = ['trainings']

class AEStudentProfileInline(admin.StackedInline):
    model = AEStudent
    filter_horizontal = ['courses']
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    model = Student
    exclude = ['options']

class ProfessorProfileInline(admin.StackedInline):
    model = Professor
    filter_horizontal = ['courses']

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor
    filter_horizontal = ['courses']

class ProfileInline(admin.StackedInline):
    model = Profile

class UserProfileAdmin(UserAdmin):
    inlines = [AEStudentProfileInline,
                ProfessorProfileInline, ProfileInline]

class TrainingAdmin(admin.ModelAdmin):
    model = Training
    filter_horizontal = ['synthesis_note', 'obligation', 'procedure', 'oral_speciality',
                         'written_speciality', 'oral_1', 'oral_2','magistral']
    exclude = ['options']

class CourseAdmin(admin.ModelAdmin):
    model = Course
    ordering = ['number']
    filter_horizontal = ['types']

class DocumentAdmin(admin.ModelAdmin):
    exclude = ['readers']
    filter_horizontal = ['course_type']
    search_fields = ['course__code', 'course__title']

class MediaAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['id', 'title', 'course__title', 'course__code']

class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['public_id', 'id', 'course__code', 'course__title']

class SeminarQuestionInline(admin.StackedInline):
    model = Question

class SeminarAdmin(admin.ModelAdmin):
    inlines = [SeminarQuestionInline,]
    exclude = ['suscribers']


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
admin.site.register(Seminar, SeminarAdmin)
admin.site.register(Question)
admin.site.register(Testimonial)
admin.site.register(TestimonialTemplate)