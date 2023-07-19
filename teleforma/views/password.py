from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (INTERNAL_RESET_SESSION_TOKEN,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView

UserModel = get_user_model()

class TFPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        label="Email ou login",
        max_length=254,
    )

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        return User.objects.filter(Q(is_active=True) & (Q(email=email) | Q(username=email)))
 
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        logins = [username for username in self.get_users(email)]
        users = self.get_users(email) 
        if users:
            user = self.get_users(email)[0]
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.email)),
                'user': user,
                'logins': logins,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )

class TFPasswordResetView(PasswordResetView):
    form_class = TFPasswordResetForm



class TFSetPasswordForm(SetPasswordForm):
    def __init__(self, users, *args, **kwargs):
        self.users = users
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        for user in self.users:
            user.set_password(password)
            if commit:
                user.save()
        return self.users


class TFPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = TFSetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = None
        self.users = self.get_users(kwargs['uidb64']) 
        token = kwargs['token']

        if self.users:
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)

                check = False                
                for user in self.users:
                    check = self.token_generator.check_token(user, session_token)
                    if check:
                        break
                
                if check:
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super(FormView, self).dispatch(*args, **kwargs)
            else:
                check = False
                for user in self.users:
                    check = self.token_generator.check_token(user, token)     
                    if check:
                        break
                if check:
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_users(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            email = urlsafe_base64_decode(uidb64).decode()
            users = User.objects.filter(email=email)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, forms.ValidationError):
            users = []
        return users
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['users'] = self.users
        return kwargs

    def form_valid(self, form):
        users = form.save()
        # get last user
        user = sorted(users, key=lambda u:u.date_joined)[0]
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super(FormView, self).form_valid(form)    