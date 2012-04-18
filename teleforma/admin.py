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

class ProfessorProfileInline(admin.StackedInline):
    model = Professor
    filter_horizontal = ['courses']

class ProfileInline(admin.StackedInline):
	model = Profile

class UserProfileAdmin(UserAdmin):
    inlines = [StudentProfileInline, ProfessorProfileInline, ProfileInline]

class TrainingAdmin(admin.ModelAdmin):
    model = Training
    filter_horizontal = ['courses']

class CourseAdmin(admin.ModelAdmin):
    model = Course

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor
    filter_horizontal = ['courses']

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Conference)
admin.site.register(IEJ)
admin.site.register(Document)
admin.site.register(Media)
admin.site.register(Room)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Procedure)
admin.site.register(Speciality)
admin.site.register(CourseType)
admin.site.register(Oral)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(StreamingServer)
admin.site.register(LiveStream)





