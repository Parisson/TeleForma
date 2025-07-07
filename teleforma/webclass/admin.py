# -*- coding: utf-8 -*-
from django.contrib import admin
from teleforma.webclass.models import (BBBServer, Webclass, WebclassRecord,
                                       WebclassSlot)


class BBBServerAdmin(admin.ModelAdmin):
    model = BBBServer
    list_display = ('url', 'api_key')

class WebclassSlotInline(admin.StackedInline):
    model = WebclassSlot
    raw_id_fields = ('participants',)
    readonly_fields = ('room_id', 'room_password')
    extra = 5

class WebclassAdmin(admin.ModelAdmin):
    inlines = [WebclassSlotInline]
    list_filter = ('course', 'period', 'iej', 'session', 'bbb_server', 'status')
    list_display = ('course', 'period', 'session', 'bbb_server', 'status')
    filter_horizontal = ('iej',)
    search_fields = ['id', 'course__code', 'course__title']

class WebclassRecordAdmin(admin.ModelAdmin):
    list_filter = ('period', 'course', 'session', 'professor', 'category', 'created', 'status')
    list_display = ('period', 'course', 'session', 'professor', 'category', 'created', 'status')
    search_fields = ['id', 'course__code', 'course__title']
    actions = ['publish',]

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(WebclassRecordAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['url'] = forms.ChoiceField(choices=get_all_records())
    #     return form

    def publish(self, request, queryset):
        for record in queryset.all():
            record.status = 3
            record.save()

    publish.short_description = "Publier les enregistrements sélectionnés"


admin.site.register(BBBServer, BBBServerAdmin)
admin.site.register(Webclass, WebclassAdmin)
admin.site.register(WebclassRecord, WebclassRecordAdmin)
