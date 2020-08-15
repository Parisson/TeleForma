# -*- coding: utf-8 -*-

import datetime
from datetime import timedelta, date
import calendar
from unidecode import unidecode

from django.db.models import *
from telemeta.models import *
from teleforma.fields import *
import django.db.models as models
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from bigbluebutton_api_python import BigBlueButton
from bigbluebutton_api_python.exception import BBBException
from jxmlease import XMLListNode, XMLDictNode

translation.activate('fr')
app_label = 'teleforma'

DAYS_CHOICES = [(i, _(calendar.day_name[i])) for i in range(7)]
# BBB_SERVER = "https://bbb.parisson.com/bigbluebutton/"
# BBB_SECRET = "uOzkrTnWly1jusr0PYcrlwhvKhZG1ZYDOrSvxgP70"
STATUS_CHOICES = (
        (2, _('Draft')),
        (3, _('Public')),
    )


class MetaCore:
    app_label = 'webclass'


def get_records_from_bbb(**kwargs):
    """get records info from bbb xml"""
    records = []
    for server in BBBServer.objects.all():
        recordings = server.get_instance().get_recordings(**kwargs).get_field('recordings')
        if hasattr(recordings, 'get'):
            recordings = recordings['recording']
        if type(recordings) is XMLDictNode:
            recordings = [recordings]
        for recording in recordings:
            recording.prettyprint()
            url = recording.get('playback', {}).get('format', {}).get('url')
            if url:
                url = url.decode()
            else:
                continue

            start = int(recording['startTime'].decode()[:-3])
            end = int(recording['endTime'].decode()[:-3])
            data = {
                'id': recording['recordID'].decode(),
                'server_id': server.id,
                'start': start,
                'start_date': datetime.datetime.fromtimestamp(start),
                'end': end,
                'end_date': datetime.datetime.fromtimestamp(end),
                'url': url,
                'preview': recording.get('playback', {}).get('format', {}).get('preview', {}).get('images', {}).get('image', [])[0].decode(),
                'state': recording['state'].decode(),
            }
            if recording['metadata'].get('periodid'):
                data.update({
                    'period_id': int(recording['metadata'].get('periodid').decode()),
                    'course_id': int(recording['metadata'].get('courseid').decode()),
                    'slot': WebclassSlot.objects.get(pk=int(recording['metadata'].get('slotid').decode()))
                })

            data['duration'] = data['end'] - data['start']
            records.append(data)
    records = sorted(records, key=lambda r:r['start'])
    return records

def get_records(period_id=None, course_id=None, rooms=None, recording_id=None):
    """ get all records, filtered """
    # if not rooms:
    #     rooms = ';'.join([slot.room_id for slot in self.slots.all()])
    # print(rooms)
    meta = {}
    if period_id:
        meta['periodid'] = period_id
    if course_id:
        meta['courseid'] = period_id
    meta['origin'] = 'crfpa'

    all_records = get_records_from_bbb(meta=meta)
    # vocabulary = [('Aucun', 'none')]
    if not all_records:
        return []

    all_records = sorted(all_records, key=lambda record:-record['start'])
    # for record in all_records:
    #     vocabulary.append((record['url'], record['start']))
    return all_records



class BBBServer(models.Model):
    url = models.CharField("Url du serveur BBB", max_length=100)
    api_key = models.CharField("API Key", max_length=100)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'bbb_server'
        verbose_name = _('BBB server')
        verbose_name_plural = _('BBB servers')

    def get_instance(self):
        return BigBlueButton(self.url, self.api_key)

    def __unicode__(self):
        return "Serveur %d" % self.id

class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(status=3).exclude(end_date__lt=date.today())

class Webclass(models.Model):

    department              = models.ForeignKey('teleforma.Department', related_name='webclass', verbose_name=_('department'), on_delete=models.SET_NULL, blank=True, null=True)
    period                  = models.ForeignKey('teleforma.Period', related_name='webclass', verbose_name=_('period'), on_delete=models.SET_NULL, blank=True, null=True)
    course                  = models.ForeignKey('teleforma.Course', related_name='webclass', verbose_name=_('course'))
    iej                     = models.ManyToManyField('teleforma.IEJ', related_name='webclass', verbose_name=_('iej'), blank=True, null=True)
    bbb_server              = models.ForeignKey('BBBServer', related_name='webclass', verbose_name='Serveur BBB')
    duration                = DurationField('Durée de la conférence', default="00:30:00")
    max_participants        = models.IntegerField('Nombre maxium de participants par créneau', blank=True, null=True, default=80)
    end_date                = models.DateField('date de fin', blank=True, null=True)
    status                  = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)

    objects = models.Manager()
    published = PublishedManager()

    class Meta(MetaCore):
        db_table = app_label + '_' + 'webclass'
        verbose_name = _('webclass')
        verbose_name_plural = _('webclass')

    def __unicode__(self):
        return "Webclass %d : %s" % (self.id, self.course.title)

    def get_slot(self, user):
        """ return webclass slot or None if user is not subscribed """
        try:
            return WebclassSlot.published.get(webclass=self, participants=user)
        except WebclassSlot.DoesNotExist:
            return None

class SlotPublishedManager(models.Manager):
    def get_query_set(self):
        return super(SlotPublishedManager, self).get_query_set().filter(webclass__status=3).exclude(webclass__end_date__lt=date.today())

class WebclassSlot(models.Model):
    """ Webclass slot """
    webclass        = models.ForeignKey('Webclass', related_name='slots')
    day             = models.IntegerField('Jour du créneau', choices=DAYS_CHOICES)
    start_hour      = models.TimeField('heure du créneau')
    professor       = models.ForeignKey('teleforma.Professor', related_name='webclass_slot', verbose_name=_('professor'),
                                 on_delete=models.SET_NULL, blank=True, null=True)
    participants    = models.ManyToManyField(User, related_name="webclass_slot", verbose_name=_('participants'),
                                        blank=True, null=True)
    room_id         = models.CharField('id de la conférence BBB (généré automatiquement)', blank=True, null=True, max_length=255)
    room_password   = models.CharField('password du modérateur (généré automatiquement)', blank=True, null=True, max_length=255)

    objects = models.Manager()
    published = SlotPublishedManager()

    class Meta(MetaCore):
        db_table = app_label + '_' + 'webclass_slot'
        verbose_name = _('webclass slot')

    def __unicode__(self):
        return "Webclass slot : " + str(self.id)


    @property
    def remaining_participant_slot(self):
        """
        get remaining participant slot
        """
        nb_participants = self.participants.count()
        return self.webclass.max_participants - nb_participants

    @property
    def participant_slot_available(self):
        """
        is there any slot available for another participants
        """
        return self.remaining_participant_slot > 0

    @property
    def end_hour(self):
        """
        start hour + duration
        """
        date = datetime.datetime.combine(datetime.date.today(), self.start_hour) + timedelta(seconds=self.webclass.duration.as_seconds())
        return date.time()

    @property
    def bbb(self):
        return self.webclass.bbb_server.get_instance()

    def prepare_webclass(self):
        """
        generate room id and moderator password
        """
        if not self.room_id:
            # not sure why, but the slug contains accent
            room_id = "%s-w%d-s%d" % (unidecode(slugify(self.webclass.course.title)), self.webclass.id, self.id)
            password = User.objects.make_random_password()
            self.room_id = room_id
            self.room_password = password
            self.save()

    def create_webclass_room(self, request):
        """ create a BBB room and generate meeting id and moderator password """
        if self.room_id:
            try:
                # check if meeting already exists
                self.get_webclass_info()
            except BBBException:
                year = datetime.datetime.now().year
                # site_url = 'https://' + request.get_host()
                webclass = self.webclass
                params = {
                    'moderatorPW':self.room_password,
                    'attendeePW':'pwattendee',
                    # 'maxParticipants':self.webclass_max_participants + 1,
                    'welcome':"Pré-Barreau : Bienvenue sur la conférence \"%s\"." % (webclass.course.title.encode('utf-8'),),
                    'record':True,
                    # 'autoStartRecording':True,
                    'muteOnStart':True,
                    'allowModsToUnmuteUsers':True,
                    # 'logo':'https://e-learning.crfpa.pre-barreau.com/static/teleforma/images/logo_pb.png',
                    'copyright': "© %d Pré-Barreau" % year,
                    # 'guestPolicy':'ALWAYS_ACCEPT'
                    'bannerText': "Pré-Barreau",
                    'bannerColor': "#003768",
                    # 'customStyleUrl': site_url+"/static/teleforma/css/bbb.css"
                }
                meta = {
                        'origin':'crfpa',
                        'periodid': webclass.period.id,
                        'courseid': webclass.course.id,
                        'webclassid': webclass.id,
                        'slotid': self.id,
                        'professor': self.professor.user.username,
                    }
                print params
                try:
                    result = self.bbb.create_meeting(self.room_id, params=params, meta=meta)
                except BBBException as e:
                    print(e)
                    raise


    def get_join_webclass_url(self, request, user, username=None):
        """
        Get url to BBB meeting.
        If user are professor or staff, provide the url with the moderator password
        """
        self.create_webclass_room(request)
        username = user.get_full_name()
        is_professor = len(user.professor.all()) >= 1
        is_staff = user.is_staff or user.is_superuser
        password = 'pwattendee'
        if is_professor or is_staff:
            password = self.room_password
        params = {'userID': user.username}
        return self.bbb.get_join_meeting_url(username, self.room_id, password, params)

    def get_fake_join_webclass_url(self, username):
        """
        Fake join url for testing purpose
        Get url to BBB meeting.
        If user are professor or staff, provide the url with the moderator password
        """
        self.create_webclass_room()
        password = 'pwattendee'
        params = {'userID': username}
        return self.bbb.get_join_meeting_url(username, self.room_id, password, params)

    def next_webclass_date(self):
        """
        get the next webclass date for this slot
        (or today webclass if this is the current day)
        """
        now = datetime.datetime.now()
        days_ahead = self.day - now.weekday()
        if days_ahead < 0:
            days_ahead += 7
        next_date = now + datetime.timedelta(days_ahead)
        next_date = next_date.replace(hour=self.start_hour.hour, minute=self.start_hour.minute)
        if self.webclass.end_date and next_date.date() > self.webclass.end_date:
            return None
        return next_date

    @property
    def status(self):
        """ is webclass running, about to start, or finished ?
        state : future, past, almost, ingoing
        """
        now = datetime.datetime.now()
        next_webclass_date_begin = self.next_webclass_date()
        if next_webclass_date_begin:
            next_webclass_date_end = next_webclass_date_begin + timedelta(seconds=self.webclass.duration.as_seconds())
        else:
            return "none"
        begin_minus_1_hour = next_webclass_date_begin - timedelta(hours=1)

        if not next_webclass_date_begin:
            return "none"
        if now < begin_minus_1_hour:
            # conference not yet started
            status = "future"
        elif next_webclass_date_end + timedelta(hours=1) < now:
            # conference expired
            status = "past"
        elif begin_minus_1_hour < now < next_webclass_date_begin:
            # conference can be joined
            status = "almost"
        else:
            status = "ingoing"
        return status

    def is_webclass_running(self):
        """ Is webclass currently running ? """
        # print(self.get_webclass_info())
        return self.bbb.is_meeting_running(self.room_id).get_field('running').decode() == 'true' or False

    def get_webclass_info(self):
        """ """
        print(self.room_id)
        print(self.bbb.get_meeting_info(self.room_id))
        return self.bbb.get_meeting_info(self.room_id)

    # def get_record(self):
    #     """ get longest published record for the current conference """
    #     all_records = []
    #     recordings = []
    #     recordings_xml = self.bbb.get_recordings(self.room_id).get_field('recordings')
    #     if hasattr(recordings_xml, 'get'):
    #         recordings = recordings_xml['recording']
    #     if type(recordings) is XMLDictNode:
    #         recordings = [recordings]
    #     for recording in recordings:
    #         recording.prettyprint()
    #         url = recording.get('playback', {}).get('format', {}).get('url')
    #         if url:
    #             url = url.decode()
    #         data = {
    #             'start': int(recording['startTime'].decode()),
    #             'end': int(recording['endTime'].decode()),
    #             'url': url,
    #             'state': recording['state'].decode(),
    #         }
    #         data['duration'] = data['end'] - data['start']
    #         all_records.append(data)

    #     if not all_records:
    #         return None
    #     all_records = sorted(all_records, key=lambda record:-record['duration'])

    #     longest_record = all_records[0]
    #     if not longest_record['url'] or longest_record['state'] != 'published':
    #         return None
    #     return longest_record


@receiver(post_save, sender=WebclassSlot)
def create_webclass_room(sender, **kwargs):
    instance = kwargs['instance']
    instance.prepare_webclass()



class WebclassRecord(models.Model):

    period                  = models.ForeignKey('teleforma.Period', verbose_name=_('period'))
    course                  = models.ForeignKey('teleforma.Course', related_name='webclass_records', verbose_name=_('course'))
    record_id               = models.CharField("Enregistrement BBB", max_length=255)
    # not used for now, but may be handy if we need to optimize performance
    bbb_server              = models.ForeignKey('BBBServer', related_name='webclass_records', verbose_name='Serveur BBB')
    created                 = models.DateTimeField("Date de la conférence", auto_now_add=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'webclass_record'
        verbose_name = 'enregistrement'
        verbose_name_plural = 'enregistrements'

    def __unicode__(self):
        return "Enregistrement webclass %d" % self.id

    @staticmethod
    def get_records(period, course):
        record_ids = set()
        for record in WebclassRecord.objects.filter(period=period, course=course):
            record_ids.add(record.record_id)
        if not record_ids:
            return []
        records = get_records_from_bbb(recording_id=','.join(record_ids))
        print(records)
        return records
