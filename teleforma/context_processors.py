# -*- coding: utf-8 -*-
# Copyright (c) 2013 Parisson SARL

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


def periods(request):
    """return the periods assigned to the user """

    user = request.user

    if not user.is_authenticated():
        return {'periods': None}
    else:
        return {'periods': get_periods(user)}



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
