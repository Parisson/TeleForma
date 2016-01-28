
from teleforma.models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from postman.utils import email_visitor, notify_user
from postman.models import Message


class StudentGroup(models.Model):
    """(Group description)"""

    name = models.CharField(_('name'), max_length=255)
    students = models.ManyToManyField(Student, related_name="groups", verbose_name=_('students'),
                                        blank=True, null=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'student_groups'

    def __unicode__(self):
        return self.name


class GroupedMessage(models.Model):
    """(GroupedMessage description)"""

    group = models.ForeignKey('StudentGroup', related_name='grouped_messages',
                                     verbose_name=_('group'),
                                     blank=True, null=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(User, related_name='grouped_messages',
                                     verbose_name=_('sender'),
                                     blank=True, null=True, on_delete=models.SET_NULL)
    subject = models.CharField(_('subject'), max_length=119)
    message = models.TextField(_('message'))
    to_send = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    date_sent = models.DateTimeField(_('date sent'), null=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'grouped_messages'

    def __unicode__(self):
        return self.group.name + ' ' + self.subject

    def save(self, *args, **kwargs):
        if self.to_sent:
            self.send()
            self.sent = True
            self.date_sent = datetime.datetime.now()
        super(GroupedMessage, self).save(*args, **kwargs)

    def send(self):
        site = Site.objects.all()[0]
        users = [student.user for student in self.group.students.all()]
        for user in users:
            mess = Message(sender=self.sender, recipient=user, subject=self.subject[:119], body=self.message)
            mess.moderation_status = 'a'
            mess.save()
            notify_user(mess, 'acceptance', site)
