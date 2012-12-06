# -*- coding: utf-8 -*-
from django.conf import settings
import socket

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
    local_ip = ''
    for interface in interfaces:
        try:
            ip = get_ip_address(interface)
            if ip:
                local_ip = ip
                break
        except:
            continue

    if not local_ip:
        local_ip = '127.0.0.1'
    return local_ip


def get_http_host(request):
    host = request.META['HTTP_HOST']
    if ':' in host:
        host = host.split(':')[0]
    return host


def host(request):
    request_host = get_http_host(request)
    local_host = get_local_host()
    
    print request_host
    print local_host

    if request_host.split('.')[0] == local_host.split('.')[0] or \
    				 request_host == '127.0.0.1' or request_host == 'localhost':
        # LAN access
        ip = local_host
    else:
        ip = settings.ROUTER_IP

    return {'HOST': ip }

