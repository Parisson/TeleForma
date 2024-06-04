# some patches for postman

from django.db import models
from django.db.models.expressions import RawSQL
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.db.models import IntegerField, Value

from postman.query import PostmanQuery
from postman.models import MessageManager, OPTION_MESSAGES

MessageManager._folder_old = MessageManager._folder

def _folder(self, related, filters, option=None, order_by=None, query_dict=None):
    """Base code, in common to the folders."""
    search = None
    if query_dict:
        search = query_dict.get('search')
    qs = self.all() if option == OPTION_MESSAGES else QuerySet(self.model, PostmanQuery(self.model), using=self._db)
    if related:
        qs = qs.select_related(*related)
    if order_by:
        qs = qs.order_by(order_by)
    if isinstance(filters, (list, tuple)):
        lookups = models.Q()
        for filter in filters:
            lookups |= models.Q(**filter)
    else:
        lookups = models.Q(**filters)

    if search:
        lookups &= models.Q(subject__icontains=search)\
                | models.Q(body__icontains=search)\
                | models.Q(sender__username__icontains=search)\
                | models.Q(sender__first_name__icontains=search)\
                | models.Q(sender__last_name__icontains=search)
    if option == OPTION_MESSAGES:
        qs = qs.filter(lookups)
        # Adding a 'count' attribute, to be similar to the by-conversation case,
        # should not be necessary. Otherwise add:
        # .extra(select={'count': 'SELECT 1'})
    else:
        qs = qs.annotate(count=RawSQL('{0}.count'.format(qs.query.pm_alias_prefix), ()))
        qs.query.pm_set_extra(table=(
            self.filter(lookups, thread_id__isnull=True).annotate(count=Value(0, IntegerField()))\
                .values_list('id', 'count').order_by(),
            # use separate annotate() to keep control of the necessary order
            self.filter(lookups, thread_id__isnull=False).values('thread').annotate(id=models.Max('pk')).annotate(count=models.Count('pk'))\
                .values_list('id', 'count').order_by(),
        ))
    if query_dict:
        limit = query_dict.get('limit')
        if limit:  # at end because doc says "Further filtering or ordering of a sliced queryset is prohibited..."
            try:
                i = int(limit)
                qs = qs[:i]
            except:  # just ignore any bad format
                pass
    return qs

MessageManager._folder = _folder