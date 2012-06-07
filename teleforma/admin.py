# -*- coding: utf-8 -*-
from teleforma.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

#class UserProfileInline(admin.StackedInline):
#	model = UserProfile

class StudentProfileInline(admin.StackedInline):
    model = Student

class StudentAdmin(admin.ModelAdmin):
    model = Student
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
                         'written_speciality', 'oral_1', 'oral_2', 'options', 'magistral']

class CourseAdmin(admin.ModelAdmin):
    model = Course

class DocumentAdmin(admin.ModelAdmin):
    exclude = ['readers']

class MediaAdmin(admin.ModelAdmin):
    exclude = ['readers']

class ConferenceAdmin(admin.ModelAdmin):
    exclude = ['readers']

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






