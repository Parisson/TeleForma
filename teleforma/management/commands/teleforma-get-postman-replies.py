# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
from postman.models import *
import re
import logging
import datetime
import time
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
import email

from teleforma import utils

import poplib

def decode_header(header, charset):
    """
    Decode a header field
    """
    header = email.header.decode_header(header)
    res = []
    for value, encoding in header:
        if isinstance(value, bytes):
            value = value.decode(encoding or charset)
        res.append(value)
    return " ".join(res)

def smart_walk(msg, in_alternative = False):
    """
    Like the walk method, but ignores html in multipart/alternative
    """
    ctype = msg.get_content_type()
    if msg.is_multipart():
        if ctype == "multipart/alternative":
            in_alternative = True
        yield msg
        subparts = msg.get_payload()
        for subpart in subparts:
            for subsubpart in smart_walk(subpart, in_alternative):
                yield subsubpart
    elif not in_alternative or not "text/html" in ctype:
        yield msg    

class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('teleforma')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Fetch mails from a POP account to feed postman"
    language_code = 'fr_FR'

    def add_arguments(self, parser):
        parser.add_argument('log_file')

    def process(self, message):
        mail = email.message_from_bytes(message)
        title = mail.get("subject", "").strip()
        title = decode_header(title, 'utf-8')
        
        parts = title.split('[')
        if len(parts) == 1:
            self.logger.warning("Invalid title (no start delimiter): {%s}" % title)
            return
        subject = '['.join(parts[:-1])
        part = parts[-1]
        if not part.endswith("]"):
            self.logger.warning("Invalid title (no start delimiter): {%s}" % title)
            return
        msghash = part[:-1]
        msgid = msghash[:-4]
        msgid = int(msgid, 16)
        if utils.generate_hash(msgid) != msghash:
            self.logger.warning("Invalid hash {%s} for {%s}" % (msghash, msgid))
            return
        msg = Message.objects.get(pk = msgid)

        self.logger.info("Found reply to message %s" % msgid)
        
        body = ""
        for part in smart_walk(mail):
            payload = part.get_payload(decode = True)
            if not isinstance(payload, bytes):
                # ignore multipart here
                continue
            filename = part.get_filename()
            content_type = part.get_content_type()
            if not filename and content_type.startswith("text/"):
                body += payload.decode(part.get_content_charset() or "ascii")
               
        # Purge quotes and signatures from body
        lines = []
        for line in body.split("\n"):
            stripped = line.strip()
            if stripped.startswith(">"):
                continue
            if stripped.startswith("----"):
                break
            if stripped.startswith("--") and not line[2:].strip():
                break
            lines.append(stripped)

        while lines and not lines[0]:
            del lines[0]
        while lines and not lines[-1]:
            del lines[-1]
        body = '\n'.join(lines)

        if not msg.thread:
            msg.thread = msg
            msg.save()

        if len(subject) > 200:
            subject = subject[:200] + "..."
        
        mess = Message(sender = msg.recipient, recipient = msg.sender,
                       subject = subject, body = body, thread = msg.thread,
                       parent = msg)
        mess.moderation_status = 'a'
        mess.save()
        site = Site.objects.all()[0]
        notify_user(mess, 'acceptance', site)
        
    def handle(self, *args, **options):
        log_file = options['log_file']
        logger = Logger(log_file)
        logger.logger.info('########### Processing #############')
        self.logger = logger.logger
        
        pop = poplib.POP3_SSL(settings.REPLY_POP_SERVER)
        pop.user(settings.REPLY_POP_LOGIN)
        pop.pass_(settings.REPLY_POP_PASSWORD)
        _, messages, _ = pop.list()
        self.logger.info("%d messages available" % len(messages))
        try:
            for msg in messages:
                msgid, _ = msg.split()
                msgid = msgid.decode('ascii')
                _, msg, _ = pop.retr(msgid)
                msg = b"\r\n".join(msg)
                try:
                    self.process(msg)
                    pop.dele(msgid)
                except Exception as e:
                    self.logger.warning("Error in message %s: %s" % (msgid, str(e)),
                                        exc_info = e)
        finally:
            pop.quit()

        self.logger.info('############## Done #################')
