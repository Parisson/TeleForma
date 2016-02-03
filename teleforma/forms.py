
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
    # first_name = forms.CharField(_('First name'), required=True)
    # last_name = forms.CharField(_('Last name'), required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', ]

RegistrationForm.base_fields.update(UserForm.base_fields)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'wifi_login', 'wifi_pass', 'language', 'expiration_date',
                    'init_password', ]

RegistrationForm.base_fields.update(ProfileForm.base_fields)


class StudentForm(ModelForm):

    def has_changed(self):
        """
        Overriding this, as the initial data passed to the form does not get noticed,
        and so does not get saved, unless it actually changes
        """
        changed_data = super(ModelForm, self).has_changed()
        return bool(self.initial or changed_data)

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
                    'init_password', 'country']


class StudentInline(InlineFormSet):

    model = Student
    can_delete = False
    fields = ['level', 'iej', 'period', 'platform_only', 'trainings', 'procedure',
                'written_speciality', 'oral_speciality', 'oral_1', 'oral_2']
