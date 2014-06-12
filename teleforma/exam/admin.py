# -*- coding: utf-8 -*-
from teleforma.admin import *
from teleforma.exam.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ScriptPageInline(admin.StackedInline):
    model = ScriptPage
    ordering = ['rank']
    extra = 10

class QuotaInline(admin.StackedInline):
    model = Quota

class CorrectorAdmin(admin.ModelAdmin):
    model = Corrector
    inlines = [QuotaInline]

class ScriptAdmin(admin.ModelAdmin):
    model = Script
    # exclude = ['options']
    # inlines = [ScriptPageInline]



admin.site.register(Corrector, CorrectorAdmin)
admin.site.register(Script, ScriptAdmin)
admin.site.register(ScriptPage)
admin.site.register(ScriptType)
admin.site.register(Quota)

