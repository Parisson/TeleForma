# -*- coding: utf-8 -*-
from teleforma.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from telemeta.models.system import UserProfile

admin.site.unregister(User)

#class UserProfileInline(admin.StackedInline):
#	model = UserProfile

class StudentProfileInline(admin.StackedInline):
    model = Student
    filter_horizontal = ['courses']

class ProfessorProfileInline(admin.StackedInline):
    model = Professor
    filter_horizontal = ['courses']

class UserProfileInline(admin.StackedInline):
	model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [StudentProfileInline, ProfessorProfileInline, UserProfileInline]

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Conference)
admin.site.register(IEJ)
admin.site.register(Document)
admin.site.register(Media)
admin.site.register(Room)
admin.site.register(User, UserProfileAdmin)





