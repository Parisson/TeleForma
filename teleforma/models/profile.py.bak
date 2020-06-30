from django.db import models
from django.contrib.auth.models import User
from teleforma.models.core import MetaCore
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
    "User profile extension"

    user            = models.ForeignKey(User, unique=True, related_name="profile")
    institution     = models.CharField(_('Institution'))
    department      = models.CharField(_('Department'))
    attachment      = models.CharField(_('Attachment'))
    function        = models.CharField(_('Function'))
    address         = models.TextField(_('Address'))
    telephone       = models.CharField(_('Telephone'))
    expiration_date = models.DateField(_('Expiration_date'))

    class Meta(MetaCore):
        db_table = 'profiles'
        permissions = (("can_not_view_users_and_profiles", "Cannot view other users and any profile"),)
