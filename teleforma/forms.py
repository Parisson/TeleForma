# -*- coding: utf-8 -*-
from StringIO import StringIO

from django.core.files.uploadedfile import SimpleUploadedFile
from models.core import Period, CourseType
from models.crfpa import IEJ, Training
from teleforma.models import *
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField, BooleanField, ImageField, CharField, \
    DateField, FileInput, ChoiceField
from django.forms.extras.widgets import SelectDateWidget
from postman.forms import WriteForm as PostmanWriteForm
from postman.fields import BasicCommaSeparatedUserField

from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from captcha.fields import CaptchaField

from teleforma.models.core import Course, Professor
from tinymce.widgets import TinyMCE
from itertools import cycle
from django.core.files.images import get_image_dimensions
from PIL import Image

LEVEL_CHOICES = [
    ('', '---------'),
    ('M1', 'M1'),
    ('M2', 'M2'),
]
TRUE_FALSE_CHOICES = (
    ('', '---------'),
    (True, 'Oui'),
    (False, 'Non')
)


def get_unique_username(first_name, last_name):
    username = slugify(first_name)[0] + '.' + slugify(last_name)
    username = username[:30]
    i = 1
    while User.objects.filter(username=username[:30]):
        username = slugify(first_name)[:i] + '.' + slugify(last_name)
        if i > len(slugify(first_name)):
            username += str(i)
        i += 1
    return username[:30]


class ConferenceForm(ModelForm):
    class Meta:
        model = Conference


#
# class RegistrationForm(ModelForm):
#     captcha = CaptchaField()
#     accept = BooleanField()
#
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'accept']


class UserForm(ModelForm):
    # profile
    address = CharField(label=_('Address'), max_length=255)
    address_detail = CharField(label=_('Address detail'), max_length=255, required=False)
    postal_code = CharField(label=_('Postal code'), max_length=255)
    city = CharField(label=_('City'), max_length=255)
    country = CharField(label=_('Country'), max_length=255)
    telephone = CharField(label=_('Telephone'), max_length=255)
    birthday = DateField(label=_('birthday'), help_text="Au format jj/mm/aaaa")
    # student
    portrait = ImageField(widget=FileInput(attrs={'accept': "image/*;capture=camera"}), required=False,
                          help_text="Veuillez utiliser une photo au format d'identité.")
    level = ChoiceField(label=_('studying level'), choices=LEVEL_CHOICES)
    iej = ModelChoiceField(label='IEJ',
                           queryset=IEJ.objects.all())
    platform_only = forms.ChoiceField(choices = TRUE_FALSE_CHOICES,
                                      label=_('e-learning platform only'),
                                      widget=forms.Select())
    period = ModelChoiceField(label='Période',
                              queryset=Period.objects.filter(is_open=True,
                                                             date_inscription_start__lte=datetime.datetime.now(),
                                                             date_inscription_end__gte=datetime.datetime.now()))
    training = ModelChoiceField(label='Formation',
                                queryset=Training.objects.filter(available=True))
    procedure = ModelChoiceField(label=_('procedure'),
                                 help_text="Matière de procédure",
                                 queryset=Course.objects.filter(procedure=True))
    written_speciality = ModelChoiceField(label=_('written speciality'),
                                          queryset=Course.objects.filter(written_speciality=True),
                                          help_text="Matière juridique de spécialité")
    oral_1 = ModelChoiceField(label=_('oral de langue (option)'),
                              help_text="Matière d’oral de langue (en option)",
                              queryset=Course.objects.filter(oral_1=True))
    promo_code = CharField(label=_('promo code'), max_length=100, required=False)
    # no model
    captcha = CaptchaField()
    accept = BooleanField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_portrait(self):
        image = self.cleaned_data['portrait']
        if not image:
            return image
        #width, height = get_image_dimensions(image)
        #ratio = float(height) / float(width)
        #if ratio > 2.5 or ratio < 1:
        #    raise ValidationError({'portrait': "L'image n'est pas au format portrait."})
        NEW_HEIGHT = 230
        NEW_WIDTH = 180
        #if width < NEW_WIDTH or height < NEW_HEIGHT:
        #    raise ValidationError({'portrait': "L'image est trop petite. Elle doit faire au moins %spx de large et %spx de hauteur." % (NEW_WIDTH, NEW_HEIGHT)})

        # resize image
        img = Image.open(image.file)
        new_image = img.resize((NEW_WIDTH, NEW_HEIGHT), Image.ANTIALIAS)

        temp = StringIO()
        new_image.save(temp, 'jpeg')
        temp.seek(0)
        return SimpleUploadedFile('temp', temp.read())

    def save(self, commit=True):

        data = self.cleaned_data
        user = super(UserForm, self).save(commit=False)
        username = get_unique_username(data['first_name'], data['last_name'])
        self.username = username
        user.username = username
        user.last_name = data['last_name'].upper()
        user.first_name = data['first_name'].capitalize()
        user.is_active = False
        if commit:
            user.save()
        profile = Profile(user=user,
                          address=data['address'],
                          address_detail=data.get('address_detail'),
                          postal_code=data['postal_code'],
                          city=data['city'],
                          country=data['country'],
                          telephone=data['telephone'],
                          birthday=data['birthday']
                          )
        if commit:
            profile.save()
        student = Student(user=user,
                          portrait=data['portrait'],
                          level=data.get('level'),
                          iej=data.get('iej'),
                          period=data.get('period'),
                          platform_only=data.get('platform_only'),
                          procedure=data.get('procedure'),
                          written_speciality=data.get('written_speciality'),
                          oral_1=data.get('oral_1'),
                          promo_code=data.get('promo_code'),
                          training=data.get('training')
                          )
        student.save()
        # student.trainings.add(*data.get('trainings', []))
        return user


# RegistrationForm.base_fields.update(UserForm.base_fields)
#
#
# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ['user', 'wifi_login', 'wifi_pass', 'language', 'expiration_date',
#                     'init_password', ]
#
# RegistrationForm.base_fields.update(ProfileForm.base_fields)
#
#
# class StudentForm(ModelForm):
#
#     class Meta:
#         model = Student
#         exclude = ['user', 'trainings', 'options']
#


#
# RegistrationForm.base_fields.update(StudentForm.base_fields)
#
#
# class CustomRegistrationForm(RegistrationForm):
#
#     def save(self, profile_callback=None):
#         user = super(CustomRegistrationForm, self).save(profile_callback=None)
#         profile, c = Profile.objects.get_or_create(user=user, \
#             address=self.cleaned_data['address'], \
#             telephone=self.cleaned_data['telephone'])
#
#
# class ProfileInline(InlineFormSet):
#
#     model = Profile
#     can_delete = False
#     exclude = ['wifi_login', 'wifi_pass', 'language', 'expiration_date',
#                     'init_password']
#
#
# class StudentInline(InlineFormSet):
#
#     model = Student
#     can_delete = False
#     fields = ['portrait', 'level', 'iej', 'period', 'training', 'platform_only', 'procedure',
#                 'written_speciality', 'oral_1', 'promo_code']
#
#     def get_factory_kwargs(self):
#         kwargs = super(StudentInline, self).get_factory_kwargs()
#
#         def get_field_qs(field, **kwargs):
#             formfield = field.formfield(**kwargs)
#             if field.name == 'period':
#                 formfield.queryset = Period.objects.filter(is_open=True)
#             elif field.name == 'portrait':
#                 formfield.widget.attrs.update(accept="image/*;capture=camera")
#                 # formfield.widget.required = True
#             return formfield
#
#         kwargs.update({
#             'formfield_callback': get_field_qs
#         })
#         return kwargs


class NewsItemForm(ModelForm):
    class Meta:
        model = NewsItem
        exclude = ['created', 'creator', 'deleted']
        widgets = {
            'description': TinyMCE({'cols': 80, 'rows': 30}),
        }


class WriteForm(PostmanWriteForm):
    recipients = BasicCommaSeparatedUserField(label=(_("Recipients"), _("Recipient")), help_text='')
    course = ModelChoiceField(queryset=Course.objects.all(), required=False)

    class Meta(PostmanWriteForm.Meta):
        fields = ('course', 'recipients', 'subject', 'body')

    def clean_recipients(self):
        """compute recipient if 'auto' is set"""
        recipients = self.cleaned_data['recipients']
        course = self.cleaned_data.get('course')
        return recipients
