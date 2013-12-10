from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins
from django.utils import translation
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import datetime


class Command(BaseCommand):
    help = """Cleanup mutiple generated testimonials per user"""
    
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        
        for user in users:
            auditor = user.auditor.all()
            professor = user.professor.all()
            seminars = []

            if auditor and not professor and user.is_active and user.email:
                auditor = auditor[0]
                context = {}
                all_seminars = auditor.seminars.all()
                
                for seminar in all_seminars:
                    testimonials = user.testimonial.filter(seminar=seminar)
                    if len(testimonials) > 1:
                        for testimonial1 in testimonials:
                            for testimonial2 in testimonials:
                                if testimonial2.date_added < testimonial1.date_added:
                                    #testimonial2.delete()
                                    print ('kept', testimonial1.title, testimonial1.date_added)
                                    print ('deleted', testimonial2.title, testimonial2.date_added)


