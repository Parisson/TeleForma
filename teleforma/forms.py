# -*- coding: utf-8 -*-
import datetime
from io import BytesIO

from captcha.fields import ReCaptchaField

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import (BooleanField, CharField, ChoiceField, DateField,
                          FileInput, ImageField, ModelChoiceField, ModelForm,
                          ModelMultipleChoiceField)
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from postman.fields import BasicCommaSeparatedUserField
from postman.forms import WriteForm as PostmanWriteForm
from tinymce.widgets import TinyMCE

from .models.core import Conference, Course, Period, payment_schedule_choices
from .models.crfpa import IEJ, PAY_STATUS_CHOICES, Corrector, NewsItem
from .models.crfpa import Profile as UserProfile
from .models.crfpa import Student, Training

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

TRAINING_TYPE = (
    ('', '---------'),
    (False, 'Formation sur place'),
    (True, 'Formation e-learning')
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


# class ConferenceForm(ModelForm):
#     class Meta:
#         model = Conference
#         fields = '__all__'


#
# class RegistrationForm(ModelForm):
#     captcha = CaptchaField()
#     accept = BooleanField()
#
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'accept']


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserForm(ModelForm):
    # profile
    address = CharField(label=_('Address'), max_length=255)
    address_detail = CharField(
        label=_('Address detail'), max_length=255, required=False)
    postal_code = CharField(label=_('Postal code'), max_length=255)
    city = CharField(label=_('City'), max_length=255)
    country = CharField(label=_('Country'), max_length=255)
    telephone = CharField(label=_('Telephone'), max_length=255)
    birthday = DateField(label=_('Birthday'), help_text="Au format jj/mm/aaaa")
    # student
    portrait = ImageField(widget=FileInput(attrs={'accept': "image/*;capture=camera"}), required=True,
                          help_text="Veuillez utiliser une photo au format d'identité.")
    level = ChoiceField(label=_('Studying level'), choices=LEVEL_CHOICES)
    iej = ModelChoiceField(label='IEJ',
                           queryset=IEJ.objects.all())
    period = ModelChoiceField(label='Période',
                              queryset=Period.objects.filter(is_open=True,
                                                             date_inscription_start__lte=datetime.datetime.now(),
                                                             date_inscription_end__gte=datetime.datetime.now()))
    platform_only = forms.ChoiceField(choices=TRAINING_TYPE,
                                      label='Type de formation',
                                      widget=forms.Select())

    training = ModelChoiceField(label='Formation',
                                queryset=Training.objects.filter(available=True))
    procedure = ModelChoiceField(label=_('Procedure'),
                                 help_text="Matière de procédure",
                                 queryset=Course.objects.filter(procedure=True))
    written_speciality = ModelChoiceField(label='Specialité écrite',
                                          queryset=Course.objects.filter(
                                              written_speciality=True),
                                          help_text="Matière juridique de spécialité")
    oral_1 = ModelChoiceField(label='Souscription à l\'oral de langue (option)',
                              help_text="Matière d’oral de langue (en option)",
                              queryset=Course.objects.filter(oral_1=True))
    promo_code = CharField(label=_('Code promo'),
                           max_length=100, required=False)

    payment_schedule = ChoiceField(label=_(u'Échéancier de paiement'),
                                   choices=payment_schedule_choices,
                                   required=True)

    fascicule = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                  label='Envoi postal des fascicules',
                                  required=False,
                                  widget=forms.Select())

    # no model
    captcha = ReCaptchaField()
    accept = BooleanField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.user_fields = ['first_name', 'last_name', 'email', 'address', 'address_detail',
                            'postal_code', 'city', 'country', 'telephone', 'birthday', 'portrait']
        self.training_fields = ['level', 'iej', 'period', 'platform_only', 'fascicule',
                                'training', 'procedure', 'written_speciality', 'oral_1']

    def clean_portrait(self):
        image = self.cleaned_data['portrait']
        if not image:
            return image
        #width, height = get_image_dimensions(image)
        #ratio = float(height) / float(width)
        # if ratio > 2.5 or ratio < 1:
        #    raise ValidationError({'portrait': "L'image n'est pas au format portrait."})
        NEW_HEIGHT = 230
        NEW_WIDTH = 180
        # if width < NEW_WIDTH or height < NEW_HEIGHT:
        #    raise ValidationError({'portrait': "L'image est trop petite. Elle doit faire au moins %spx de large et %spx de hauteur." % (NEW_WIDTH, NEW_HEIGHT)})

        # resize image
        img = Image.open(image.file)
        new_image = img.resize((NEW_WIDTH, NEW_HEIGHT), Image.ANTIALIAS)
        if new_image.mode == "RGBA":
            new_image = new_image.convert("RGB")

        temp = BytesIO()
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
        profile = UserProfile(user=user,
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
        platform_only = data.get('platform_only') == 'True' and True or False
        fascicule = data.get('fascicule') == 'True' and True or False
        training = data.get('training')
        subscription_fees = 0
        if platform_only:
            if fascicule:
                subscription_fees = training.cost_elearning_fascicle
            else:
                subscription_fees = training.cost_elearning_nofascicle
        else:
            subscription_fees = training.cost
        student = Student(user=user,
                          portrait=data['portrait'],
                          level=data.get('level'),
                          iej=data.get('iej'),
                          period=data.get('period'),
                          platform_only=platform_only,
                          procedure=data.get('procedure'),
                          written_speciality=data.get('written_speciality'),
                          oral_1=data.get('oral_1'),
                          promo_code=data.get('promo_code'),
                          training=training,
                          payment_schedule=data.get('payment_schedule'),
                          fascicule=fascicule,
                          subscription_fees=subscription_fees
                          )
        student.save()
        student.trainings.add(data.get('training', None))
        return user


class CorrectorForm(ModelForm):
    # profile
    address = CharField(label=_('Address'), max_length=255)
    address_detail = CharField(
        label=_('Address detail'), max_length=255, required=False)
    postal_code = CharField(label=_('Postal code'), max_length=255)
    city = CharField(label=_('City'), max_length=255)
    country = CharField(label=_('Country'), max_length=255)
    telephone = CharField(label=_('Telephone'), max_length=255)
    birthday = DateField(label=_('Birthday'), help_text="Au format jj/mm/aaaa")
    birthday_place = CharField(label='Lieu de naissance', max_length=255)
    nationality = CharField(label='Nationalité', max_length=255)
    ss_number = CharField(label='N° de sécurité sociale',
                          max_length=15)
    siret = CharField(label='N° SIRET',
                      max_length=13, required=False)
    # corrector
    period = ModelChoiceField(label='Période',
                              queryset=Period.objects.filter(is_open=True,
                                                             date_inscription_start__lte=datetime.datetime.now(),
                                                             date_inscription_end__gte=datetime.datetime.now()))
    pay_status = forms.ChoiceField(choices=PAY_STATUS_CHOICES,
                                   label='Statut',
                                   widget=forms.Select())
    courses = ModelMultipleChoiceField(label='Matière',
                                       queryset=Course.objects.all().exclude(title="Aucune").order_by('title'),
                                       widget=forms.CheckboxSelectMultiple())
    # no model
    captcha = ReCaptchaField()
    # accept = BooleanField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(CorrectorForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.user_fields = ['first_name', 'last_name', 'email', 'address', 'address_detail', 'postal_code',
                            'city', 'country', 'telephone', 'birthday', 'birthday_place', 'nationality', 'ss_number', 'siret']
        self.training_fields = ['courses', 'period', 'pay_status']

    def clean_siret(self):
        if self.data['pay_status'] == 'honoraires' and not self.cleaned_data['siret'].strip():
            raise ValidationError(
                "Le SIRET est obligatoire si vous choississez le statut honoraires")
        return self.data['siret']

    def save(self, commit=True):

        data = self.cleaned_data
        user = super(CorrectorForm, self).save(commit=False)
        username = get_unique_username(data['first_name'], data['last_name'])
        self.username = username
        user.username = username
        user.last_name = data['last_name'].upper()
        user.first_name = data['first_name'].capitalize()
        user.is_active = False
        if commit:
            user.save()
        profile = UserProfile(user=user,
                              address=data['address'],
                              address_detail=data.get('address_detail'),
                              postal_code=data['postal_code'],
                              city=data['city'],
                              country=data['country'],
                              telephone=data['telephone'],
                              birthday=data['birthday'],
                              birthday_place=data['birthday_place'],
                              ss_number=data['ss_number'],
                              siret=data['siret'],
                              nationality=data['nationality']
                              )
        if commit:
            profile.save()
        corrector = Corrector(user=user,
                              period=data.get('period'),
                              pay_status=data.get('pay_status'),
                              )
        corrector.save()
        corrector.courses.set(data.get('courses'))
        return user


class NewsItemForm(ModelForm):
    class Meta:
        model = NewsItem
        exclude = ['created', 'creator', 'deleted']
        widgets = {
            'description': TinyMCE({'cols': 80, 'rows': 30}),
        }


class WriteForm(PostmanWriteForm):
    recipients = BasicCommaSeparatedUserField(
        label=(_("Recipients"), _("Recipient")), help_text='')
    course = ModelChoiceField(queryset=Course.objects.all(), required=False)

    class Meta(PostmanWriteForm.Meta):
        fields = ('course', 'recipients', 'subject', 'body')

    def clean_recipients(self):
        """compute recipient if 'auto' is set"""
        recipients = self.cleaned_data['recipients']
        return recipients
