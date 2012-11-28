# -*- coding: utf-8 -*-
from teleforma.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


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
    filter_horizontal = ['seminars']

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

class MediaAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['id']

class MediaPackageAdmin(admin.ModelAdmin):
    exclude = ['readers', 'mime_type']
    search_fields = ['id']

class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['public_id', 'id']

class SeminarQuestionInline(admin.StackedInline):
    model = Question

class SeminarAdmin(admin.ModelAdmin):
    inlines = [SeminarQuestionInline,]
    filter_horizontal = ['professor', 'media', 'media_preview', 
                         'doc_1', 'doc_2', 'doc_correct']


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Period)
# admin.site.register(Training, TrainingAdmin)

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType)
admin.site.register(Conference, ConferenceAdmin)
# admin.site.register(IEJ)

admin.site.register(Seminar, SeminarAdmin)
admin.site.register(Question)
admin.site.register(Testimonial)
admin.site.register(TestimonialTemplate)
admin.site.register(SeminarType)

admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentType)
# admin.site.register(Media, MediaAdmin)
admin.site.register(MediaPackage, MediaPackageAdmin)
admin.site.register(Room)

admin.site.register(StreamingServer)
admin.site.register(LiveStream)

