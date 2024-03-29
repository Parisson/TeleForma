# -*- coding: utf-8 -*-
# Copyright (c) 2011-2012 Parisson SARL

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


from ..models.core import Course, CourseType
from .core import format_courses


def get_ae_courses(user, date_order=False, num_order=False):
    courses = []

    if not user.is_authenticated:
        return None

    professor = user.professor.all()
    student = user.ae_student.all()
    types = CourseType.objects.all()

    if professor:
        professor = user.professor.get()
        courses = format_courses(courses, queryset=professor.courses.all(),
                                 types=types)

    elif student:
        student = user.ae_student.get()
        s_courses = student.courses.all()

        for course in s_courses:
            courses = format_courses(courses, course=course,
                                     types=types)

        magistrals = Course.objects.filter(magistral=True)
        if magistrals:
            courses = format_courses(courses,
                                     queryset=magistrals,
                                     types=types)

    elif user.is_staff or user.is_superuser:
        courses = format_courses(courses, queryset=Course.objects.all(),
                                 types=types)
    else:
        courses = None

    if date_order:
        courses = sorted(courses, key=lambda k: k['date'], reverse=True)
    if num_order:
        courses = sorted(courses, key=lambda k: k['number'])

    return courses
