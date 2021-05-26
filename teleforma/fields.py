
import datetime
import re

import django.db.models as models
from django import forms
from django.contrib.auth import get_user_model
from django.core import exceptions
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _


class ShortTextField(models.TextField):

    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": Textarea(attrs={'rows':2, 'cols':40})}
         )
         return super(ShortTextField, self).formfield(**kwargs)



class Duration(object):
    """Represent a time duration"""
    def __init__(self, *args, **kwargs):
        if len(args) and isinstance(args[0], datetime.timedelta):
            self._delta = datetime.timedelta(days=args[0].days, seconds=args[0].seconds)
        else:
            self._delta = datetime.timedelta(*args, **kwargs)

    def __decorate(self, method, other):
        if isinstance(other, Duration):
            res = method(other._delta)
        else:
            res = method(other)
        if type(res) == datetime.timedelta:
            return Duration(res)

        return res

    def __add__(self, other):
        return self.__decorate(self._delta.__add__, other)

    def __nonzero__(self):
        return self._delta.__nonzero__()

    def __str__(self):
        hours   = self._delta.days * 24 + self._delta.seconds / 3600
        minutes = (self._delta.seconds % 3600) / 60
        seconds = self._delta.seconds % 60

        return "%.2d:%.2d:%.2d" % (hours, minutes, seconds)

    @staticmethod
    def fromstr(str):
        if not str:
            return Duration()

        test = re.match('^([0-9]+)(?::([0-9]+)(?::([0-9]+))?)?$', str)
        if test:
            groups = test.groups()
            try:
                hours = minutes = seconds = 0
                if groups[0]:
                    hours = int(groups[0])
                    if groups[1]:
                        minutes = int(groups[1])
                        if groups[2]:
                            seconds = int(groups[2])

                return Duration(hours=hours, minutes=minutes, seconds=seconds)
            except TypeError:
                print(groups)
                raise
        else:
            raise ValueError("Malformed duration string: " + str)

    def as_seconds(self):
        return self._delta.days * 24 * 3600 + self._delta.seconds


def normalize_field(args, default_value=None):
    """Normalize field constructor arguments, so that the field is marked blank=True
       and has a default value by default.

       This behaviour can be disabled by passing the special argument required=True.

       The default value can also be overriden with the default=value argument.
       """
    required = False
    if 'required' in args:
        required = args['required']
        args.pop('required')

    args['blank'] = not required

    if not required:
        if 'default' not in args:
            if args.get('null'):
                args['default'] = None
            elif default_value is not None:
                args['default'] = default_value

    return args


# The following is based on Django TimeField
class DurationField(models.Field):
    """Duration Django model field. Essentially the same as a TimeField, but
    with values over 24h allowed.

    The constructor arguments are also normalized with normalize_field().
    """

    description = _("Duration")

    # __metaclass__ = models.SubfieldBase

    default_error_messages = {
        'invalid': _('Enter a valid duration in HH:MM[:ss] format.'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **normalize_field(kwargs, '0'))

    def db_type(self, connection):
        return 'int'
        
    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, int):
            return Duration(seconds=value)
        if isinstance(value, datetime.time):
            return Duration(hours=value.hour, minutes=value.minute, seconds=value.second)
        if isinstance(value, datetime.datetime):
            # Not usually a good idea to pass in a datetime here (it loses
            # information), but this can be a side-effect of interacting with a
            # database backend (e.g. Oracle), so we'll be accommodating.
            return self.to_python(value.time())
        else:
            value = str(value)
        try:
            return Duration.fromstr(value)
        except ValueError:
            raise exceptions.ValidationError(self.error_messages['invalid'])

    def get_prep_value(self, value):
        return self.to_python(value)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        # Casts times into the format expected by the backend
        try:
            return value.as_seconds()
        except:
            return value

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            data = str(val)
        return data

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CharField}
        defaults.update(kwargs)
        return super(DurationField, self).formfield(**defaults)
