# -*- coding: utf-8 -*-
from teleforma.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class StudentProfileInline(admin.StackedInline):
    model = Student
    filter_horizontal = ['period']
    exclude = ['options']

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
    inlines = [StudentProfileInline, ProfessorProfileInline, ProfileInline]

class TrainingAdmin(admin.ModelAdmin):
    model = Training
    filter_horizontal = ['synthesis_note', 'obligation', 'procedure', 'oral_speciality',
                         'written_speciality', 'oral_1', 'oral_2','magistral']
    exclude = ['options']

class CourseAdmin(admin.ModelAdmin):
    model = Course
    ordering = ['number']

class DocumentAdmin(admin.ModelAdmin):
    exclude = ['readers']
    filter_horizontal = ['course_type']

class MediaAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['id']

class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers']
    search_fields = ['public_id', 'id']


admin.site.unregister(User)
admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Period)
admin.site.register(Course, CourseAdmin)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(IEJ)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentType)
admin.site.register(Media, MediaAdmin)
admin.site.register(Room)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(CourseType)
admin.site.register(StreamingServer)
admin.site.register(LiveStream)
admin.site.register(Payment)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
