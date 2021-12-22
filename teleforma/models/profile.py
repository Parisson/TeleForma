from django.db import models
from django.contrib.auth.models import User
from teleforma.models.core import MetaCore
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    "User profile extension"

    user            = models.ForeignKey(User, on_delete=models.CASCADE,  unique=True, related_name="profile")
    institution     = models.CharField(_('Institution'), max_length=255)
    department      = models.CharField(_('Department'), max_length=255)
    attachment      = models.CharField(_('Attachment'), max_length=255)
    function        = models.CharField(_('Function'), max_length=255)
    address         = models.TextField(_('Address'))
    telephone       = models.CharField(_('Telephone'), max_length=255)
    expiration_date = models.DateField(_('Expiration_date'))

    class Meta(MetaCore):
        db_table = 'profiles'
        permissions = (("can_not_view_users_and_profiles", "Cannot view other users and any profile"),)
