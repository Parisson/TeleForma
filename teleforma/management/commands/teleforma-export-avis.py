from django.core.management.base import BaseCommand
from teleforma.models import Testimonial, Conference
from pbcart.models import Cart

import logging
from datetime import datetime, timedelta, date
import csv
import StringIO
from ftplib import FTP


class Command(BaseCommand):
    help = "Send orders to avis-verifies ftp"
    args = 'days'
    FTP_HOST = "global-ftp.netreviews.eu"
    FTP_PORT = 22
    FTP_LOGIN = "fr_pro-barreau.com"
    FTP_PASSWORD = "pd8ExNC3"
    FTP_PATH = "/orders/"

    
    def handle(self, *args, **options):
        days = int(args[0])
        logging.info('Generate csv file...')
        logging.info('Generate csv file done')

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
        for testimonial in testimonials:
            user = testimonial.user
            # find relevant cart
            cart = None
            if testimonial.seminar.course.code == "demo":
                continue
            for cart in Cart.objects.filter(user=testimonial.user, status=Cart.STATE_PAYMENT_ACCEPTED).all():
                if cart.has_item(testimonial.seminar):
                    break
            if not cart:
                logging.warning("Can't find cart for testimonial %d" % testimonial.id)
                continue

            if not testimonial.seminar.product_code:
                logging.warning("No product code for seminar %d" % testimonial.seminar.id)
                continue
            cart_date = cart.date_payment
            if not cart_date:
                cart_date = cart.last_updated
            print("add")
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
                logging.warning("No product code for conference %d" % conference.id)
                continue
            for auditor in conference.auditor.all():
                cart = None
                user = auditor.user
                for cart in Cart.objects.filter(user=user, status=Cart.STATE_PAYMENT_ACCEPTED).all():
                    if cart.has_item(conference):
                        break
                
                if not cart:
                    logging.warning("Can't find cart for conference %d" % conference.id)
                    continue
                cart_date = cart.date_payment
                if not cart_date:
                    cart_date = cart.last_updated
                print("add conf")
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
        print(output.getvalue())
        output.seek(0)

        logging.info('Sending csv to ftp...')

        ftp = FTP(self.FTP_HOST)
        try:
            
            ftp.login(self.FTP_LOGIN, self.FTP_PASSWORD)
            ftp.cwd(self.FTP_PATH)
            ftp.storlines("STOR export-orders%s.csv" % str(date.today()), output)
            ftp.quit()
        except:
            ftp.close()
            logging.error('Error while uploading to FTP')
            raise
        logging.info('Sending csv to ftp done')


