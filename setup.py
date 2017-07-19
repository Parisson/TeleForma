# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

CLASSIFIERS = ['Environment :: Web Environment', 'Framework :: Django', 'Intended Audience :: Education', 'Programming Language :: Python', 'Programming Language :: JavaScript', 'Topic :: Internet :: WWW/HTTP :: Dynamic Content', 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application', 'Topic :: Multimedia :: Sound/Audio', 'Topic :: Multimedia :: Sound/Audio :: Analysis', 'Topic :: Multimedia :: Sound/Audio :: Players', 'Topic :: Scientific/Engineering :: Information Analysis', 'Topic :: System :: Archiving',  ]

setup(
  name = "TeleForma",
  url = "https://github.com/yomguy/teleforma",
  description = "open web multimedia e-learning platform",
  long_description = open('README.rst').read(),
  author = "Guillaume Pellerin",
  author_email = "yomguy@parisson.com",
  version = '1.1',
  install_requires = [
        'django==1.4.19',
        'telemeta==1.4.6',
        'south',
        'django-pagination==1.0.7',
        'django-postman==3.2.0',
        'django-extensions==0.9',
        'django-notes',
        'django-timezones==0.2',
        'django-jqchat',
        'crocodoc',
        'django-registration==0.8',
        'django-extra-views==0.6.5',
        'django-simple-captcha',
        'django-suit',
        'django-nvd3',
        'django-user-agents',
        'xhtml2pdf',
        'html5lib==0.95',

  ],
  platforms=['OS Independent'],
  license='CeCILL v2',
  classifiers = CLASSIFIERS,
  packages = find_packages(),
  include_package_data = True,
  zip_safe = False,
)
