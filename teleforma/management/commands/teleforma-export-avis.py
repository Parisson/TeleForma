from django.core.management.base import BaseCommand
from optparse import make_option
from django.core.mail import send_mail
from django.conf import settings

from teleforma.models import Testimonial, Conference
from pbcart.models import Cart

import logging
from datetime import datetime, timedelta, date
import csv
import StringIO
from ftplib import FTP

from teleforma.context_processors import seminar_validated
from teleforma.views.pro import get_seminar_delta

class Command(BaseCommand):
    help = "Send orders to avis-verifies ftp"
    args = 'days'
    option_list = BaseCommand.option_list + (
        make_option('--dry-run', action='store_true',
            help='Do not send to ftp / mail'),
    )
    FTP_HOST = "global-ftp.netreviews.eu"
    FTP_PORT = 22
    FTP_LOGIN = "fr_pro-barreau.com"
    FTP_PASSWORD = "pd8ExNC3"
    FTP_PATH = "/orders/"

    
    def log(self, message):
        print(message)
        logging.info(message)
        self.logs += message + "\n"

    def handle(self, *args, **options):
        self.logs = ""
        days = int(args[0])
        dry_run = options['dry_run']
        print(dry_run)
        logging.info('Generate csv file...')

        output = StringIO.StringIO()
        writer = csv.writer(output, delimiter=';')
        
        writer.writerow([
            "order_ref", 
            "email", 
            "order_date",
            "firstname",
            "lastname",
            "id_product",
            "name_product"
        ])

        # get testimonials created within X days
        delay = datetime.now() - timedelta(days=days)
        testimonials = Testimonial.objects.filter(date_added__gte=delay)

        added = []
        testimonial_not_ok = []
        cart_not_found = []
        no_product_code = []

        for testimonial in testimonials:
            user = testimonial.user
            seminar = testimonial.seminar
            if testimonial.seminar.course.code == "demo":
                continue
            # https://mattermost.pilotsystems.net/pro-barreau/pl/twdx8ro6mfbimyr7n31tkpstac
            # testimonials are created before being accessible
            if not seminar_validated(user, seminar) or not (get_seminar_delta(user, seminar) >= 0):
                testimonial_not_ok.append(user)
                continue
            # find relevant cart
            cart = None

            for some_cart in Cart.objects.filter(user=testimonial.user, status=Cart.STATE_PAYMENT_ACCEPTED).all():
                if some_cart.has_item(testimonial.seminar):
                    cart = some_cart
            if not cart:
                cart_not_found.append(user)
                # if this is a seminar linked to a conference, it's normal we don't find it in the cart
                if not testimonial.seminar.conference:
                    self.log("Can't find cart for testimonial %d and user %s" % (testimonial.id, str(user)))
                continue

            if not testimonial.seminar.product_code:
                no_product_code.append(user)
                self.log("No product code for seminar %d" % testimonial.seminar.id)
                continue
            cart_date = cart.date_payment
            if not cart_date:
                cart_date = cart.last_updated
            added.append(user)
            writer.writerow([
                cart.order_id,                              # order reference
                user.email,                                 # customer email 
                cart_date.strftime('%Y-%m-%d'),             # order date (YYYY-MM-DD hh:mm:ss OR YYYY-MM-DD)
                user.first_name.encode('utf-8'),            # customer firstname
                user.last_name.encode('utf-8'),             # customer lastname
                testimonial.seminar.product_code,           # id of the product
                testimonial.seminar.title.encode('utf-8')   # name of the product
            ])
        

        for conference in Conference.objects.filter(date_end__gte=delay, date_end__lt=datetime.now()):
            if not conference.product_code:
                self.log("No product code for conference %d" % conference.id)
                no_product_code.append(user)
                continue
            for auditor in conference.auditor.all():
                cart = None
                user = auditor.user
                for some_cart in Cart.objects.filter(user=user, status=Cart.STATE_PAYMENT_ACCEPTED).all():
                    if some_cart.has_item(conference):
                        cart = some_cart
                
                if not cart:
                    self.log("Can't find cart for conference %d and user %s" % (conference.id, str(user)))
                    cart_not_found.append(user)
                    continue
                cart_date = cart.date_payment
                if not cart_date:
                    cart_date = cart.last_updated

                added.append(user)
                writer.writerow([
                    cart.order_id,                              # order reference
                    user.email,                                 # customer email 
                    cart_date.strftime('%Y-%m-%d'),             # order date (YYYY-MM-DD hh:mm:ss OR YYYY-MM-DD)
                    user.first_name.encode('utf-8'),            # customer firstname
                    user.last_name.encode('utf-8'),             # customer lastname
                    conference.product_code,           # id of the product
                    conference.title.encode('utf-8')   # name of the product
                ])
        # import pdb;pdb.set_trace()

        self.log("\n")
        self.log("Added :")
        self.log("\n".join([str(user) for user in added]))
        self.log("\n")

        if testimonial_not_ok:
            self.log("Testimonial not validated :")
            self.log("\n".join([str(user) for user in testimonial_not_ok]))
            self.log("\n")

        if cart_not_found:
            self.log("Cart not found :")
            self.log("\n".join([str(user) for user in cart_not_found]))
            self.log("\n")

        if no_product_code:
            self.log("No product code :")
            self.log("\n".join([str(user) for user in no_product_code]))
            self.log("\n")

        self.log("Generated file :")
        self.log(output.getvalue())
        output.seek(0)

        if not dry_run:
            self.log('Sending csv to ftp...')
            ftp = FTP(self.FTP_HOST)
            try:
                ftp.login(self.FTP_LOGIN, self.FTP_PASSWORD)
                ftp.cwd(self.FTP_PATH)
                ftp.storlines("STOR export-orders%s.csv" % str(date.today()), output)
                ftp.quit()
            except:
                ftp.close()
                self.log('Error while uploading to FTP')
                raise
            self.log('Sending csv to ftp done')

            send_mail(
                "Rapport export d'avis",
                self.logs,
                settings.DEFAULT_FROM_EMAIL,
                settings.REPORT_TO_EMAIL,
                fail_silently=False,
            )
