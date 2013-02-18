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

class CourseDomainAdmin(admin.ModelAdmin):
    filter_horizontal = ['courses']

class DocumentAdmin(admin.ModelAdmin):
    exclude = ['readers']
    filter_horizontal = ['course_type']
    search_fields = ['title']

class MediaAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['id', 'title', 'course__title', 'course__code']

class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['public_id', 'id']
    filter_horizontal = ['docs_description']

class SeminarQuestionInline(admin.StackedInline):
    model = Question

class SeminarAdmin(admin.ModelAdmin):
    inlines = [SeminarQuestionInline,]
    filter_horizontal = ['professor', 'medias', 'docs_description',
                         'docs_1', 'docs_2', 'docs_correct']
    ordering = ['course', 'rank']
    search_fields = ['course__title', 'title', 'sub_title']

    class Media:
        css = { 'all': ('admin/extra.css',) }

class MediaItemMarkerAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

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
admin.site.register(Testimonial)
admin.site.register(TestimonialTemplate)
admin.site.register(SeminarType)
admin.site.register(Answer)

admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentType)
admin.site.register(Media, MediaAdmin)
admin.site.register(Room)

admin.site.register(StreamingServer)
admin.site.register(LiveStream)

# TELEMETA
admin.site.register(MediaItemMarker, MediaItemMarkerAdmin)

