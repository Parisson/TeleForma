#!/usr/bin/python

import pandas as pd
import requests
from subprocess import check_output, CalledProcessError
domain_prod = "http://brahms.ircam.fr"
domain_dev = "http://localhost:9030"
session_option = "-H 'Cookie: sessionid={0}'"
session_prod = "gd9zgu68wo3lptwfhqqkawo59w0486rz"
session_dev = "qh25niyvxetuouxwmafdpvxlc8eldp5u"

analyse_urls = [
    # analyse - published
    "/analyses/dialogue/",
    "/analyses/metallics/",
    "/analyses/noanoa/",
    "/analyses/traiettoria/",
    "/analyses/Mortuos/",
    "/analyses/Stria/",
    "/analyses/Prologue/",
    # analyse - draft
    "/analyses/Etymo/",
    "/analyses/EnTrance/",
    "/analyses/test/",
    "/analyses/test2/",
    # composer
    "/witold-lutoslawski",
    "/wlodzimierz-kotonski",
    "/omer-hulusier",
    "/necil-kazim-akses",
    "/wenjing-guo",
    "/rene-alix",
    "/axel-borup-jrgensen",
    "/per-nrgard",
    "/pierre-boulez",
    # events_event      
    "/admin/events/event/13/change/",
    "/admin/events/event/23/change/",
    #events_hall  
    "/admin/events/hall/5/change/",
    #events_manifestation
    "/admin/events/manifestation/3/change/",
    #repertoire_analysis_definitions
    "/admin/repertoire/definition/32/change/",
    #robots_rule  
    "/admin/robots/rule/1/change/",
    #robots_url
    "/admin/robots/url/3/change/",
    #utils_citysidney
    "/admin/utils/citysidney/3/change/",
    #utils_corporatebody
    "/admin/utils/corporatebody/127/change/",
    #utils_countrysidney
    "/admin/utils/countrysidney/230/change/",
    #utils_equipmentbrand
    "/admin/utils/equipmentbrand/127/change/",
    #utils_equipmentcategory
    "admin/utils/equipmentcategory/4/change/",
    #utils_equipmentreference
    "/admin/utils/equipmentreference/422/change/",
    #utils_error  
    "/admin/utils/error/1703/change/",
    #utils_lang   
    "/admin/utils/lang/1/change/",
    #utils_naturalperson
    "/admin/utils/naturalperson/6791/change/",
    "/admin/utils/naturalperson/6806/change/",
    "/admin/utils/naturalperson/6892/change/",
    #utils_personfunction   
    "/admin/utils/personfunction/12/change/",
    #validation_fichedevalidation
    "/admin/validation/fichedevalidation/74/change/",
    "/admin/validation/fichedevalidation/63/change/",
    #works_electronic
    "/admin/works/electronic/11/change/",
    "/admin/works/electronic/5/change/",
    #works_filetype
    "/admin/works/filetype/20/change/",
    #works_version
    "/admin/works/version/1345/change/",
    "/admin/works/version/990/change/",
    #works_versionfile
    "/admin/works/versionfile/2665/change/",
    "/admin/works/versionfile/9250/change/",
    #works_worksidney
    "/admin/works/worksidney/6970/change/",
    "/admin/works/worksidney/18566/change/",
    "/admin/works/worksidney/7549/change/",
    "/admin/works/worksidney/25673/change/",
    "/admin/works/worksidney/10575/change/",
]

def get_curl_command(domain, url, session):
    return "curl -s '{0}' {1}".format(domain + url, session_option.format(session))

for url in analyse_urls:
    print("==========================================================================")
    print("url ", url)
    print("-----------------------------------------")
    try:
        curl_prod = get_curl_command(domain_prod, url, session_prod)
        curl_dev = get_curl_command(domain_dev, url, session_dev)
        check_output("diff <("+curl_prod+") <("+ curl_dev + ")",
                    shell=True, executable='/bin/bash', universal_newlines=True)
    except CalledProcessError as e:
        print(e.output, e.returncode)

