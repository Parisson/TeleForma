==========================================
TeleForma : open web e-learning platform
==========================================

Key features
============

 * User management and registration
 * School data model (trainings, courses, course types, professors, etc...)
 * Video and audio LIVE conferencing (with TeleCaster devices)
 * Media streaming and document management of various types
 * Live chat room auto-creation for every conference created
 * Embedded messaging system
 * Media analyzing and indexing (thanks to Telemeta)

It is based on Django and fully written in Python, HTML5, CSS and JavaScript.

keywords: social e-learning, live conferencing, hypermedia private access


News
====

0.8
+++++

 * First release! see the features ;)


Screenshots
===========

See http://files.parisson.org/gallery/main.php/v/Screenshots/teleforma/


Installation
============

Teleforma is exclusively based on open-source modules.

The best way to get in run and test is to install it in a virtualenv with pip::

    sudo apt-get install python-pip python-gst0.10
    sudo pip install virtualenv
    virtualenv --system-site-packages teleforma
    bin/pip install teleforma



Bugs and feedback
=================

You are welcome to freely use this application in accordance with its licence.
If you find some bugs, PLEASE leave a ticket on this page:

https://github.com/yomguy/teleforma/issues

You can also leave a ticket to request some new interesting features for the next versions.
And even if Telemeta suits you, please give us some feedback !


Related projects
================

 * `Telemeta <http://telemeta.org>`_ - open web audio CMS
 * `TimeSide <http://code.google.com/p/timeside/>`_ - open web audio components


Contact
=======

Homepage : https://github.com/yomguy/teleforma

E-mail : Guillaume Pellerin <yomguy@parisson.com>

Twitter : http://twitter.com/parisson_studio

Google+ : +Parisson


Development
===========

You are welcome to participate to the development of the TeleForma project.

To get the lastest development version, you need git and run::

    git clone git://github.com/yomguy/teleforma.git


License
=======

CeCILL v2, compatible with GPL v2 (see `LICENSE <https://github.com/yomguy/teleforma/blob/master/LICENSE>`_)

