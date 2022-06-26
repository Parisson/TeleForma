
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..models import MetaCore
from ..models.core import app_label
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save

def in_one_week():
    return datetime.utcnow() + timedelta(days=7)

def notify(users, message, url, days_before_expiration=None):
    """
    Notify users with message / url
    """
    if isinstance(users, User):
        users = [users,]
    for user in users:
        notif = Notification(user=user, message=message, url=url)
        if days_before_expiration:
            notif.expired = datetime.utcnow() + timedelta(days=days_before_expiration)
        notif.save()

class Notification(models.Model):
    """A notification message"""

    message = models.CharField('Message', max_length=255)
    url = models.CharField('Url', max_length=255)
    user = models.ForeignKey(
        User, related_name='notifications', verbose_name=_('user'), on_delete=models.CASCADE)
    viewed = models.BooleanField("Vu", default=False)
    created = models.DateTimeField('Creation date', auto_now_add=True)
    expired = models.DateTimeField("Date d'expiration", default=in_one_week)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'notifications'

    def __str__(self):
        return f"{str(self.user)} - {self.message[:20]}"

    def broadcast(self):
        """
        broadcast a notification to socket
        """
        print("broadcast")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"notifications_{self.user.id}", {
            'type': 'notify',
            'message': self.to_dict()
        })

    def to_dict(self):
        return {
            '_id': self.id,
            'content': self.message,
            'url': self.url,
            'date': self.created.strftime('%d/%m/%Y'),
            'created': str(self.created),
            'viewed': self.viewed
        }



def save_notification(sender, instance, **kwargs):
    instance.broadcast()

post_save.connect(save_notification, sender=Notification)