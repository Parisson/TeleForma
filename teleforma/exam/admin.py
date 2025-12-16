# -*- coding: utf-8 -*-
import os

from django.contrib import admin
from django.http import HttpResponse
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.models import User
from django.db.models import Q
from xlwt import Workbook

from ..exam.models import Quota, Script, ScriptPage, ScriptType


class QuotaAdmin(admin.ModelAdmin):
    model= Quota
    list_display = ['corrector_name', 'course', 'period', 'session', 'script_type', 'date_start', 'date_end',
                    'pending_script_count', 'marked_script_count',
                    'all_script_count', 'value', 'level']
    list_filter = ['course__title', 'period', 'session']
    search_fields = ['corrector__username', 'corrector__last_name']

    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['corrector'].queryset = User.objects.filter(is_active=True).filter(Q(corrector__isnull=False) | Q(is_superuser=True))
         return super(QuotaAdmin, self).render_change_form(request, context, *args, **kwargs)

    def corrector_name(self, instance):
        if instance.corrector:
            return instance.corrector.last_name + ' ' + instance.corrector.first_name
        else:
            return "Aucun"


class ScriptPageInline(admin.StackedInline):
    model = ScriptPage
    ordering = ['rank']
    extra = 10


class QuotaInline(admin.StackedInline):
    model = Quota


class ScriptAdmin(admin.ModelAdmin):
    model = Script
    ordering = ['-date_added']
    search_fields = ['=author__username', 'author__last_name', '=corrector__username',
                    'corrector__last_name', 'course__title', 'course__code']
    readonly_fields = ['date_added','uuid','box_uuid','sha1','mime_type']
    autocomplete_fields = ['author']
    list_filter = ['period', 'course__title', 'session', 'type', 'status',
                    'date_submitted', 'date_marked', 'date_rejected',
                   'author__student__platform_only']
    list_display = ['title', 'author_name', 'corrector', 'file_size', 'status']
    actions = ['force_resubmit', 'export_xls']

    class Media:
        js = ("exam/js/admin.js",)


    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['corrector'].queryset = User.objects.filter(is_active=True).filter(Q(corrector__isnull=False) | Q(is_superuser=True) | Q(professor__isnull=False)).order_by('last_name')
         return super(ScriptAdmin, self).render_change_form(request, context, *args, **kwargs)

    def author_name(self, instance):
        if instance.author:
            return instance.author.username
        else:
            return 'None'

    def file_size(self, instance):
        if instance.file:
            if os.path.exists(instance.file.path):
                return filesizeformat(os.stat(instance.file.path).st_size)
            else:
                return '0'
        else:
            return '0'

    def force_resubmit(self, request, queryset):
        for script in queryset.all():
            script.status = 2
            script.corrector = None
            script.date_marked = None
            script.date_rejected = None
            script.url = ''
            script.box_uuid = ''
            script.save()

    force_resubmit.short_description = "Re-submit scripts"

    def export_xls(self, request, queryset):
        book = Workbook()
        sheet = book.add_sheet('Scripts')

        # En-têtes
        cols = [
            {'name': 'Identifiant', 'width': 5000},
            {'name': 'Matière', 'width': 8000},
            {'name': 'Séance', 'width': 3000},
            {'name': 'Note', 'width': 3000},
        ]
        row = sheet.row(0)
        for i, col in enumerate(cols):
            row.write(i, col['name'])
            sheet.col(i).width = col['width']

        # Données
        for i, script in enumerate(queryset):
            row = sheet.row(i + 1)
            row.write(0, script.author.username if script.author else '')
            row.write(1, script.course.title if script.course else '')
            row.write(2, script.session or '')
            row.write(3, script.score if script.score is not None else '')

        response = HttpResponse(content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=scripts.xls'
        book.save(response)
        return response

    export_xls.short_description = "Export vers XLS"


admin.site.register(Script, ScriptAdmin)
admin.site.register(ScriptPage)
admin.site.register(ScriptType)
admin.site.register(Quota, QuotaAdmin)
