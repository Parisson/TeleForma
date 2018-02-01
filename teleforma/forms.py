from django.forms import ModelForm
from teleforma.models import *
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from captcha.fields import CaptchaField


class ConferenceForm(ModelForm):

    class Meta:
        model = Conference


class UserForm(ModelForm):

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]


RegistrationForm.base_fields.update(UserForm.base_fields)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'wifi_login', 'wifi_pass', 'language', 'expiration_date',
                    'init_password', ]

RegistrationForm.base_fields.update(ProfileForm.base_fields)


class StudentForm(ModelForm):

    class Meta:
        model = Student
        exclude = ['user', 'trainings', 'options']



RegistrationForm.base_fields.update(StudentForm.base_fields)


class CustomRegistrationForm(RegistrationForm):

    def save(self, profile_callback=None):
        user = super(CustomRegistrationForm, self).save(profile_callback=None)
        profile, c = Profile.objects.get_or_create(user=user, \
            address=self.cleaned_data['address'], \
            telephone=self.cleaned_data['telephone'])


class ProfileInline(InlineFormSet):

    model = Profile
    can_delete = False
    exclude = ['wifi_login', 'wifi_pass', 'language', 'expiration_date',
                    'init_password']


class StudentInline(InlineFormSet):

    model = Student
    can_delete = False
    fields = ['level', 'iej', 'period', 'training', 'platform_only', 'procedure',
                'written_speciality', 'oral_1', 'promo_code']

    def get_factory_kwargs(self):
        kwargs = super(StudentInline, self).get_factory_kwargs()

        def get_field_qs(field, **kwargs):
            formfield = field.formfield(**kwargs)
            if field.name == 'period':
                formfield.queryset = Period.objects.filter(is_open=True)
            return formfield

        kwargs.update({
            'formfield_callback': get_field_qs
        })
        return kwargs