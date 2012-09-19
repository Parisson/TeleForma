=========
TeleForma
=========

Teleforma is an open source web e-learning platform.

keywords: social e-learning, live conferencing, hypermedia private access

It is based on Django and fully written in Python, HTML5, CSS and JavaScript.

News
====

0.8
+++++

 * First release! see the features ;)


Key features
============

 * User management and registration
 * School data model (trainings, courses, course types, professors, etc...)
 * Video and audio LIVE conferencing (with TeleCaster devices)
 * Media streaming and document management of various types
 * Live chat room auto-creation for every conference created
 * Embedded messaging system
 * Media analyzing and indexing (thanks to Telemeta)


Installation
============

Teleforma is exclusively based on open-source modules.

The best way to get in run and test is to install it in a virtualenv with pip::

    $ sudo apt-get install python-pip python-gst0.10
    $ sudo pip install virtualenv
    $ virtualenv --system-site-packages teleforma
    $ bin/pip install teleforma


Demo
====

http://teleforma.parisson.com

login: demo
password: demo


Bugs and feedback
=================

You are welcome to freely use this application in accordance with its licence.
If you find some bugs, PLEASE leave a ticket on this page:

http://telemeta.org/newticket

You can also leave a ticket to request some new interesting features for the next versions.
And even if Telemeta suits you, please give us some feedback !


Related projects
================

`TimeSide <http://code.google.com/p/timeside/>`_ - Web Audio Components

    a python library library to compute audio analysis, transcode, and streaming to browsers.



Contact
=======

Homepage: http://telemeta.org

E-mails:

 * Guillaume Pellerin <yomguy@parisson.com>,
 * Olivier Guilyardi <olivier@samalyse.com>,
 * Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>

Twitter:

 * http://twitter.com/telemeta
 * http://twitter.com/parisson_studio


Development
===========

You are welcome to participate to the development of the Telemeta project.

To get the lastest development version, you need subversion and run::

    $ git clone http://vcs.parisson.com/git/telemeta.git

License
=======

CeCILL v2, compatible with GPL v2 (see `LICENSE <http://github.com/yomguy/Telemeta/blob/master/LICENSE>`_)

