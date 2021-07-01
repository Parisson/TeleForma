  
from django.contrib import admin


class MultipleChoiceListFilter(admin.SimpleListFilter):
    template = 'admin/multiselect.html'


    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.used_parameters[self.parameter_name] = request.GET.getlist(self.parameter_name) or []
        lookup_choices = self.lookups(request, model_admin)
        if lookup_choices is None:
            lookup_choices = ()
        self.lookup_choices = list(lookup_choices)


    def lookups(self, request, model_admin):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError(
            'The MultipleChoiceListFilter.lookups() method must be overridden to '
            'return a list of tuples (value, verbose value).'
        )

    def queryset(self, request, queryset):
        if request.GET.get(self.parameter_name):
            kwargs = {self.parameter_name: request.GET.getlist(self.parameter_name)}
            queryset = queryset.filter(**kwargs)
        return queryset


    def choices(self, changelist):

        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() and str(lookup) in self.value(),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }