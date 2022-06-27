
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _

from ..models import MetaCore
from ..models.core import app_label
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ChatMessage(models.Model):
    """A chat message"""

    message = models.CharField('Message', max_length=255)
    room_name = models.CharField('Salon', max_length=255)
    user = models.ForeignKey(
        User, related_name='chat_messages', verbose_name=_('user'), on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField('Creation date', auto_now_add=True)
    system = models.BooleanField(default=False)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'chat_messages'

    def __str__(self):
        return f"{str(self.user)} - {self.room_name} - {self.message[:20]}"

    @classmethod
    def add_message(cls, user, room_name, message, system=False):
        message = ChatMessage(user=user, message=message,
                              room_name=room_name, system=system)
        message.save()
        return message.to_dict()

    @classmethod
    def get_room_name(cls, period, course=None):
        if course:
            return f"period{period.id}_course{course.id}"
        else:
            return f"period{period.id}_global"

    @classmethod
    def live_conference_message(cls, conference):
        """
        broadcast a live message
        """
        room_name = ChatMessage.get_room_name(
            conference.period, conference.course)
        text = _("A new live conference has started : ")
        text += f"https://{Site.objects.all()[0].domain}{reverse('teleforma-conference-detail', kwargs={'period_id': conference.period.id, 'pk': conference.id})}"
        message = ChatMessage.add_message(
            None, room_name, text, system=True)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"chat_{room_name}", {
            'type': 'chat_message',
            'message': message
        })

    def to_dict(self):
        return {
            '_id': self.id,
            'content': self.message,
            'senderId': self.user and self.user.id or "system",
            'username': self.user and self.user.username or "Système",
            'date': '13 November',
            'timestamp': '10:20',
            'date': self.created.strftime('%d/%m/%Y'),
            'timestamp': self.created.strftime('%H:%M'),
            'system': self.system
        }
