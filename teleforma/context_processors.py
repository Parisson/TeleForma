# -*- coding: utf-8 -*-
# Copyright (c) 2012 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Authors: Guillaume Pellerin <yomguy@parisson.com>


from teleforma.views.core import *

from django.conf import settings
import socket
import fcntl
import struct

interfaces = ['eth0', 'eth1', 'eth2', 'eth0-eth2', 'eth3', 'eth4',
                  'wlan0', 'wlan1', 'wlan2', 'wlan3', 'wlan4']

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])
    return ip

def get_local_host():
    ip = ''
    for interface in interfaces:
        try:
            ip = get_ip_address(interface)
            if ip:
                local_ip = ip
                break
        except:
            local_ip = '127.0.0.1'
    return local_ip


def get_http_host(request):
    host = request.META['REMOTE_ADDR']
    if ':' in host:
        host = host.split(':')[0]
    return host


def host(request):
    request_host = get_http_host(request)
    local_host = get_local_host()
    
    if request_host.split('.')[0] == local_host.split('.')[0] or \
                                 request_host == '127.0.0.1' or request_host == 'localhost':
        # LAN access
        ip = local_host
    else:
        ip = settings.ROUTER_IP

    return {'HOST': ip }


def seminar_progress(user, seminar):    
    """return the user progress of a seminar in percent
    """

    progress = 0
    total = 0
    
    objects = [seminar.docs_1, seminar.docs_2, seminar.medias, seminar.docs_correct]
    for obj in objects:
        for item in obj.all():
            total += item.weight
            if user in item.readers.all():
                progress += item.weight
    
    questions = Question.objects.filter(seminar=seminar, status=3)
    for question in questions:
        total += question.weight
        answer = Answer.objects.filter(question=question, status=3, user=user)
        if answer:
            progress += question.weight

    if total != 0:
        return int(progress*100/total)
    else:
        return 0

def seminar_validated(user, seminar):
    validated = []
    questions = seminar.question.filter(status=3)
    if questions:
        for question in questions:
            answers = Answer.objects.filter(question=question, user=user, validated=True)
            if answers:
                validated.append(True)
            else:
                validated.append(False)
        return not False in validated
    return False

def all_seminars(request, progress_order=False, date_order=False):
    seminars = []

    if isinstance(request, User):
        user = request
    else:
        user = request.user
    
    if not user.is_authenticated():
        return {}

    professor = user.professor.all()
    auditor = user.auditor.all()

    if professor:
        seminars = []
        professor = user.professor.get()
        courses = professor.courses.all()
        
        for course in courses:
            for seminar in course.seminar.all():
                seminars.append(seminar)

    elif auditor and not (user.is_staff or user.is_superuser):
        auditor = user.auditor.get()
        seminars = auditor.seminars.all()

    elif user.is_staff or user.is_superuser:
        seminars = Seminar.objects.all()
    else:
        seminars = {}

    if seminars and progress_order == True:
        s_list = [{'seminar': seminar, 'progress': seminar_progress(user, seminar)} for seminar in seminars]
        seminars = sorted(s_list, key=lambda k: k['progress'], reverse=False)
        seminars = [s['seminar'] for s in seminars]

    if seminars and date_order == True:
        s_list = []
        for seminar in seminars:
            revisions = SeminarRevision.objects.filter(user=user, seminar=seminar)
            if revisions:
                s_list.append({'seminar': seminar, 'date': revisions[0].date})
            else:
                s_list.append({'seminar': seminar, 'date': datetime.datetime.min})
        seminars = sorted(s_list, key=lambda k: k['date'], reverse=True)
        seminars = [s['seminar'] for s in seminars]

    return {'all_seminars': seminars}


def total_progress(request):
    """return the user progress of all seminars in percent"""

    user = request.user
    progress = 0

    if not user.is_authenticated():
        return {'total_progress': 0}

    auditor = user.auditor.all()
    professor = user.professor.all()

    if auditor and not (user.is_staff or user.is_superuser):
        seminars = auditor[0].seminars.all()        
    elif user.is_superuser or user.is_staff:
        seminars = Seminar.objects.all()
    elif professor:
        seminars = all_seminars(request)['all_seminars']
    else:
        seminars = None

    for seminar in seminars:
        progress += seminar_progress(user, seminar)

    if seminars:
        return {'total_progress': int(progress/len(seminars))}
    else:
        return {'total_progress': 0}

        
