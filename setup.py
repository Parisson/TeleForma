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
  version = '0.8',
  install_requires = [
        'django>=1.4',
        'telemeta',
        'south',
        'django-pagination',
        'django-postman',
        'django-extensions',
        'django-notes',
        'django-timezones',
  ],
  platforms=['OS Independent'],
  license='CeCILL v2',
  classifiers = CLASSIFIERS,
  packages = find_packages(),
  include_package_data = True,
  zip_safe = False,
)
