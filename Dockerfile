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

FROM parisson/telemeta:latest

MAINTAINER Guillaume Pellerin <yomguy@parisson.com>

RUN mkdir /srv/app
RUN mkdir /srv/src
RUN mkdir /srv/src/app

COPY . /srv/src/app
WORKDIR /srv/src/app
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt --src /srv/src
WORKDIR /srv/app

EXPOSE 8000
