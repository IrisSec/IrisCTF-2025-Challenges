# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM python:3.13.1-slim-bookworm as chroot

RUN cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/sources-src.sources
RUN sed -i 's|Types: deb|Types: deb-src|g' /etc/apt/sources.list.d/sources-src.sources
RUN apt-get update

WORKDIR /root

RUN apt update && apt install -y dpkg-dev gperf && apt source python3-seccomp
RUN python3 -m pip install cython
RUN cd libseccomp-2.5.4/ && ./configure && make && make install
RUN cd libseccomp-2.5.4/src/python && python3 -m pip install setuptools && VERSION_RELEASE=2.5.4 python3 -m pip install . --no-build-isolation
RUN rm -rf *

RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY flag.txt flag.txt
RUN sh -c 'dst=$(head -c 10 /dev/urandom | base32); mkdir /$dst; mv flag.txt /$dst/flag.txt' 
COPY jail.py /home/user/

CMD /usr/local/bin/python3 /home/user/jail.py
