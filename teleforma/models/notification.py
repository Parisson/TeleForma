
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _

from ..models import MetaCore
from ..models.core import app_label
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def in_one_week():
    return datetime.utcnow() + timedelta(days=1)

class Notification(models.Model):
    """A notification message"""

    message = models.CharField('Message', max_length=255)
    url = models.CharField('Url', max_length=255)
    user = models.ForeignKey(
        User, related_name='notifications', verbose_name=_('user'), on_delete=models.CASCADE)
    created = models.DateTimeField('Creation date', auto_now_add=True)
    expired = models.DateTimeField("Date d'expiration", default=in_one_week)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'notifications'

    def __str__(self):
        return f"{str(self.user)} - {self.message[:20]}"

    @classmethod
    def create(cls, user, room_name, message, system=False):
        notification = Notification(user=user, message=message,
                              room_name=room_name, system=system)
        notification.save()
        return notification.to_dict()
    
    def broadcast(self):
        """
        broadcast a notification to socket
        """
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(f"usernotification_{self.user.id}", {
            'type': 'notification',
            'message': self.to_dict()
        })

    def to_dict(self):
        return {
            '_id': self.id,
            'content': self.message,
            'url': self.url,
            'date': self.created.strftime('%d/%m/%Y'),
        }
