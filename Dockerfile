# Copyright 2013 Thatcher Peskens
# Copyright 2014-2015 Guillaume Pellerin
# Copyright 2014-2015 Thomas Fillon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.9

MAINTAINER Guillaume Pellerin <yomguy@parisson.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /srv/app

WORKDIR /srv

RUN apt-get update && apt-get install -y apt-transport-https
# COPY etc/apt/sources.list /etc/apt/
COPY debian-packages.txt /srv
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" /srv/debian-packages.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    echo fr_FR.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen && \
    apt-get clean

ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

# https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    PIP_CACHE_DIR="/root/.cache/pip"

ENV PATH="$POETRY_HOME/bin:$PATH"

# # Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

# upgrade pip and pin setuptools
# RUN pip3 install "setuptools<58.0.0"
RUN pip3 install -U pip
# RUN pip3 install setuptools==58

# Disable Poetry's virtualenv (useless in a container)
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /srv/

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip poetry install --no-interaction

COPY lib /srv/lib
COPY bin/build/local/setup_lib.sh /srv
RUN /srv/setup_lib.sh

COPY sherlocks /srv/sherlocks
RUN ln -s /srv/app/sherlocks-param /srv/sherlocks/param

WORKDIR /srv/src/teleforma
COPY setup.py /srv/src/teleforma
COPY teleforma /srv/src/teleforma
COPY README.rst /srv/src/teleforma
RUN python setup.py develop

# Workaround for django installation bugs
# RUN cp -ra /usr/local/django/* /usr/local/lib/python2.7/site-packages/django/
# RUN cp -ra /usr/local/django_extensions/* /usr/local/lib/python2.7/site-packages/django_extensions/

WORKDIR /srv/app

EXPOSE 8000
