# -*- coding: utf-8 -*-
from teleforma.models import *
from django.contrib import admin

class StudentAdmin(admin.ModelAdmin):
    search_fields = ['user', 'iej']
    ordering = ['user']
    filter_horizontal = ['courses']

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Professor)
admin.site.register(Conference)
admin.site.register(IEJ)
admin.site.register(Student, StudentAdmin)
admin.site.register(Document)
admin.site.register(Video)
admin.site.register(Audio)








