# -*- coding: utf-8 -*-
from teleforma.admin import *
from teleforma.exam.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.template.defaultfilters import filesizeformat


class QuotaAdmin(admin.ModelAdmin):
    model= Quota
    list_display = ['corrector_name', 'course', 'script_type', 'date_start', 'date_end',
                    'pending_script_count', 'marked_script_count',
                    'all_script_count', 'value', 'level']
    list_filter = ['course__title']
    search_fields = ['corrector__username', 'corrector__last_name']

    def corrector_name(self, instance):
        return instance.corrector.last_name + ' ' + instance.corrector.first_name


class ScriptPageInline(admin.StackedInline):
    model = ScriptPage
    ordering = ['rank']
    extra = 10


class QuotaInline(admin.StackedInline):
    model = Quota


class ScriptAdmin(admin.ModelAdmin):
    model = Script
    ordering = ['-date_added']
    search_fields = ['author__username', 'author__last_name', 'corrector__username',
                    'corrector__last_name', 'course__title', 'course__code']
    readonly_fields = ['date_added','uuid','box_uuid','sha1','mime_type']
    list_filter = ['period', 'course__title', 'session', 'type', 'status']
    list_display = ['title', 'author_name', 'file_size', 'status']

    def author_name(self, instance):
        return instance.author.username

    def file_size(self, instance):
        if instance.file:
            if os.path.exists(instance.file.path):
                print instance.file.path
                return filesizeformat(os.stat(instance.file.path).st_size)
            else:
                return '0'
        else:
            return '0'


admin.site.register(Script, ScriptAdmin)
admin.site.register(ScriptPage)
admin.site.register(ScriptType)
admin.site.register(Quota, QuotaAdmin)

